import asyncio
import base64
import os
import re
import tempfile
import uuid
from pathlib import Path

MAX_DOWNLOAD_RECORDS_PER_TAB = 20
MAX_DOWNLOAD_INLINE_BYTES = 20 * 1024 * 1024


def sanitize_filename(value: str) -> str:
    name = str(value or "download.bin")
    name = re.sub(r'[\\/:*?"<>|\x00-\x1F]', "_", name).strip()
    return name[:200] or "download.bin"


def guess_mime_type_from_name(value: str) -> str:
    v = str(value or "").lower()
    if v.endswith(".png"):
        return "image/png"
    if v.endswith(".jpg") or v.endswith(".jpeg"):
        return "image/jpeg"
    if v.endswith(".webp"):
        return "image/webp"
    if v.endswith(".gif"):
        return "image/gif"
    if v.endswith(".svg"):
        return "image/svg+xml"
    return "application/octet-stream"


async def remove_download_file_if_present(record):
    file_path = record.get("filePath")
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            pass


async def trim_tab_downloads(tab_state):
    while len(tab_state["downloads"]) > MAX_DOWNLOAD_RECORDS_PER_TAB:
        stale = tab_state["downloads"].pop(0)
        await remove_download_file_if_present(stale)


async def clear_tab_downloads(tab_state):
    entries = list(tab_state.get("downloads", []))
    tab_state["downloads"] = []
    await asyncio.gather(*[remove_download_file_if_present(e) for e in entries])


async def clear_session_downloads(session):
    if not session or "tabGroups" not in session:
        return
    tasks = []
    for group in session["tabGroups"].values():
        for tab_state in group.values():
            tasks.append(clear_tab_downloads(tab_state))
    await asyncio.gather(*tasks)


def attach_download_listener(tab_state, tab_id, log):
    if tab_state.get("downloadListenerAttached"):
        return

    tab_state["downloadListenerAttached"] = True

    async def handle_download(download):
        download_id = str(uuid.uuid4())
        suggested = sanitize_filename(download.suggested_filename or f"download-{download_id}.bin")

        file_path = os.path.join(tempfile.gettempdir(), f"camofox-download-{download_id}-{suggested}")

        failure = None
        bytes_size = None

        try:
            await download.save_as(file_path)
            stat = os.stat(file_path)
            bytes_size = stat.st_size
        except Exception as err:
            failure = str(err)
            if os.path.exists(file_path):
                os.remove(file_path)

        try:
            reported_failure = await download.failure()
            if reported_failure:
                failure = reported_failure
        except:
            pass

        url = download.url or ""
        if url:
            tab_state.setdefault("visitedUrls", set()).add(url)

        mime_type = guess_mime_type_from_name(suggested)

        tab_state.setdefault("downloads", []).append(
            {
                "id": download_id,
                "tabId": tab_id,
                "url": url,
                "suggestedFilename": suggested,
                "mimeType": mime_type,
                "bytes": bytes_size,
                "createdAt": asyncio.get_event_loop().time(),
                "filePath": None if failure else file_path,
                "failure": failure,
            }
        )

        await trim_tab_downloads(tab_state)

        log(
            "info",
            "download captured",
            {
                "tabId": tab_id,
                "downloadId": download_id,
                "suggestedFilename": suggested,
                "mimeType": mime_type,
                "bytes": bytes_size,
                "failure": failure,
            },
        )

    tab_state["page"].on("download", lambda d: asyncio.create_task(handle_download(d)))


async def get_downloads_list(tab_state, include_data=False, max_bytes=MAX_DOWNLOAD_INLINE_BYTES):
    snapshot = list(tab_state.get("downloads", []))
    results = []

    for entry in snapshot:
        item = {
            "id": entry["id"],
            "url": entry["url"],
            "suggestedFilename": entry["suggestedFilename"],
            "mimeType": entry["mimeType"],
            "bytes": entry["bytes"],
            "createdAt": entry["createdAt"],
            "failure": entry["failure"],
        }

        if include_data and entry.get("filePath") and not entry.get("failure"):
            if entry["bytes"] and entry["bytes"] > max_bytes:
                item["dataSkipped"] = "max_bytes_exceeded"
            else:
                try:
                    with open(entry["filePath"], "rb") as f:
                        raw = f.read()
                    item["dataBase64"] = base64.b64encode(raw).decode()
                except Exception as err:
                    item["readError"] = str(err)

        results.append(item)

    return results


async def extract_page_images(page, include_data=False, max_bytes=MAX_DOWNLOAD_INLINE_BYTES, limit=8):
    return await page.evaluate(
        """async ({ includeData, maxBytes, limit }) => {

        const toDataUrl = (blob) =>
          new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result || "");
            reader.onerror = () => reject("file_reader_failed");
            reader.readAsDataURL(blob);
          });

        const nodes = Array.from(document.querySelectorAll('img'));
        const seen = new Set();
        const results = [];

        for (const node of nodes) {
          const src = (node.currentSrc || node.src || node.getAttribute('src') || '').trim();
          if (!src || seen.has(src)) continue;
          seen.add(src);

          const entry = {
            src,
            alt: node.alt || "",
            width: node.naturalWidth || node.width,
            height: node.naturalHeight || node.height
          };

          if (includeData) {
            try {
              if (src.startsWith('data:')) {
                entry.dataUrl = src;
              } else {
                const res = await fetch(src);
                if (res.ok) {
                  const blob = await res.blob();
                  if (blob.size <= maxBytes) {
                    entry.dataUrl = await toDataUrl(blob);
                  } else {
                    entry.dataSkipped = "max_bytes_exceeded";
                  }
                }
              }
            } catch (e) {
              entry.fetchError = String(e);
            }
          }

          results.push(entry);
          if (results.length >= limit) break;
        }

        return results;
        }""",
        {"includeData": include_data, "maxBytes": max_bytes, "limit": limit},
    )

