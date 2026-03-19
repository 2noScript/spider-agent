


from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Optional, Dict, Union
from fastapi import Form



class TabsRequest(BaseModel):
    userId: str | None = None


class BaseRequestModel(BaseModel):
    archer_cookie: str = Field(default="")
    target_user_id: Union[str, int] = Field(default="")

    class Config:
        json_schema_extra = {
            "example": {
                "archer_cookie": "tt_chain_token=mvL/lmn17Qiz3ct10Lg8qg==; delay_guest_mode_vid=8; fbm_1862952583919182=base_domain=.www.tiktok.com; d_ticket=5bccb5b88fc8bd19a3028c99b57da81d5f09c; ttwid=1%7CKZnaIsRKXB01eDqrvBoT5-uSOcDVaLCCuvRQ93m64yU%7C1745002064%7Cbb27bce0855c2103509efb64accf2feb466f0b99377508fccf4f6373a1278d85; _ga=GA1.1.838012618.1746579444; _ga_LWWPCY99PB=GS1.1.1746581759.2.0.1746581759.0.0.774280846; _tt_enable_cookie=1; from_way=paid; tta_attr_id_mirror=0.1747383352.7504954349848969217; _yjsu_yjad=1748029415.46a3928f-c27a-4412-93eb-477add1cbd05; _gtmeec=e30%3D; ttcsid_C97F413C77U6S6FS3KBG=1748029415738::NmZbrGw8XKcET9BulKUh.1.1748029422804; ttcsid_C97F14JC77U63IDI7U40=1748029415739::H6PoZ-xRTt8FNgS-sLaJ.1.1748029422804; ttcsid_C97F65JC77UB71TGK1OG=1748029415739::Js1J5kQxC_F7HrBNksc4.1.1748029422804; ttcsid_C97F83JC77UC6ALACM60=1748029415739::7-EKoxvj-RW3asn23Tej.1.1748029422805; ttcsid_C97F9QBC77U37LFVJTOG=1748029415739::rT5pOARymoBc1tZIlyEU.1.1748029422805; ttcsid_CDICPPBC77UFUTJBVLI0=1748029415914::E8Vs5T4MRYpqS55E7mwJ.1.1748029422805; ttcsid_CS7J93RC77U6TI82IEB0=1748029415927::mGC-UZADI5i8ntOtH0Hs.1.1748029422805; ttcsid_CBUS2N3C77UB6N0891N0=1748029415937::d-8eR2Srf8TAmabHpwdU.1.1748029422806; ttcsid_CGCP5PJC77U5LCHF3VG0=1748029415941::nwd0p8zvI3dN8XA5mut8.1.1748029422806; _ga_HV1FL86553=GS1.1.1748029415.1.1.1748029443.0.0.651138025; _ga_R5EYE54KWQ=GS1.1.1748029415.1.1.1748029443.0.0.620614736; d_ticket_ads=a22f30eb1062b75746d4481855791cbd5f09c; sid_guard_ads=8f7a6742f870ca5ffe883399f9be5cbd%7C1748213056%7C5183999%7CThu%2C+24-Jul-2025+22%3A44%3A15+GMT; _fbp=fb.1.1748213205894.1481826544; living_user_id=209632895245; _ttp=2xXge4GNOarZwzujgSmsEdxRZ3X.tt.1; sid_guard_tiktokseller=c73a1344914af729243a98ba9f896a09%7C1750172867%7C3224190%7CThu%2C+24-Jul-2025+22%3A44%3A17+GMT; ttcsid_CMSS13RC77U1PJEFQUB0=1750172866412::uP37B8u2RVosxYOVBOvZ.3.1750172893965; ttcsid=1750172866413::_Uxknlhit8WIGNowVKqB.4.1750172893965; _gcl_aw=GCL.1750172905.CjwKCAjwpMTCBhA-EiwA_-MsmfmSCuFZUbFTgJsRcaLWtTYDz_CD7tl9LYRgu1GMnY8sqqTyPY5QkRoCgmQQAvD_BwE; _gcl_gs=2.1.k1$i1750172904$u51132715; _ga_BZBQ2QHQSP=GS2.1.s1750172865$o3$g1$t1750172905$j0$l0$h458571879; FPGCLAW=2.1.kCjwKCAjwpMTCBhA-EiwA_-MsmfmSCuFZUbFTgJsRcaLWtTYDz_CD7tl9LYRgu1GMnY8sqqTyPY5QkRoCgmQQAvD_BwE$i1750172906; FPGCLGS=2.1.k1$i1750172904$u51132715; _ga_NBFTJ2P3P3=GS1.1.1750172911.3.1.1750173400.0.0.1666603310; store-country-code=vn; store-country-code-src=uid; tt-target-idc=alisg; last_login_method=QRcode; tt_csrf_token=oQCcdQON-fYFgTreY1fFrxe-K5Kd1kITx3fk; s_v_web_id=verify_mdom9u10_Bm5J5Xr9_QU4X_4exK_AIWf_OGTrBhRRiTSv; passport_fe_beating_status=true; csrf_session_id=da0811a436c1c65604c4b08aa0869a74; multi_sids=6625030902617604098%3A7d03b671421a022ad81bc3e365a7abf7; cmpl_token=AgQQAPOFF-RO0ovOOCbAsNk7_Zaci23Lf5YOYN2vRw; sid_guard=7d03b671421a022ad81bc3e365a7abf7%7C1754598947%7C15552000%7CTue%2C+03-Feb-2026+20%3A35%3A47+GMT; uid_tt=ac9ddf79512cdfc18221cd2628ab600643ba3b02c78b4b0990f118ff72245c69; uid_tt_ss=ac9ddf79512cdfc18221cd2628ab600643ba3b02c78b4b0990f118ff72245c69; sid_tt=7d03b671421a022ad81bc3e365a7abf7; sessionid=7d03b671421a022ad81bc3e365a7abf7; sessionid_ss=7d03b671421a022ad81bc3e365a7abf7; sid_ucp_v1=1.0.0-KDExNjMwMzQ1MTIwMTkxZGJhYTEyZWQzNzZhOTJmYThlNTM2ZmQ5ODgKGgiCgIjElNC1-FsQo5zUxAYYsws4B0D0B0gEEAMaBm1hbGl2YSIgN2QwM2I2NzE0MjFhMDIyYWQ4MWJjM2UzNjVhN2FiZjc; ssid_ucp_v1=1.0.0-KDExNjMwMzQ1MTIwMTkxZGJhYTEyZWQzNzZhOTJmYThlNTM2ZmQ5ODgKGgiCgIjElNC1-FsQo5zUxAYYsws4B0D0B0gEEAMaBm1hbGl2YSIgN2QwM2I2NzE0MjFhMDIyYWQ4MWJjM2UzNjVhN2FiZjc; store-idc=alisg; tt-target-idc-sign=LtYRcz31S1kBELakkxh7Aij3Fvg3N5bPoRbGQSwKOVpHjbZhuL2Ltw4EHT2eGubEaw-O8DyCXlXQ34tvEVIGpesEU3s0-MUXW6MTZ31hRw8gLSZ9vy5il5AWk7a3dlVP6PIe2TVhGNEZ2Qbgwjjtt-ny0q3bNsqRb48GiFx3gc545vhTNc59xhs3VfapagnPxlAhSOslrwILrzZKGjx6Lb8y0BvLvb4bj2n2Wmh22WckrrSqAW9IQV1d9aLnihlIiPwINO-G5BPCRnXx4kCYPMTCD-h1ERHzxYdP0Ryc4W3nfmVDcAMpXg57-xJcdXY6zSUB8ZqS91mB9C5Bc_Z6I_gazlGWCY5ySiOg42clXgheynCxR9g_AWPK5WeVvkQZdXVLXjG6DM-9bJkQkC1rwNVWS-Eo1PElL2zua9faAlYoGVq6sLK3zrkdxBVllB5EjLFdvDA9G5bL-7iWG_yTUHmL9rVfsiRCgYzz7SzC-fE-hBe_Fl3co7g-m8sjx-2Z; __tea_cache_tokens_1988={%22user_unique_id%22:%227491462796246533652%22%2C%22timestamp%22:1754965099643%2C%22_type_%22:%22default%22}; gd_random=eyJtYXRjaCI6ZmFsc2UsInBlcmNlbnQiOjAuMzA3MjgyMjEwNTUyNTE2OH0=.pwuLhI+7Bpxy0xcb7DzD1Gn09YSm8PR/ZhInwP2Xwcw=; _tea_utm_cache_1988={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; _tea_utm_cache_594856={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; _tea_utm_cache_548444={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; _tea_utm_cache_345918={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}; perf_feed_cache={%22expireTimestamp%22:1756800000000%2C%22itemIds%22:[%227539073348077096210%22%2C%227539508393560526100%22%2C%227521639462955158791%22]}; store-country-sign=MEIEDN0DuZq6a3vXQhUt6gQgpiXkZeIrPDlsNobwFj3tsKykVw62Mto7vX38FT3oiYsEEKcG5RLDwpum5qIqYj-l8e4; odin_tt=4288298e18a25d5c9df6a487f0cff9283e170c1ef0375d8b26e44057fbffbfa0ef651cfa3007ad584f3681faa29b0d42e0786bf114f61b42ec12755ffec6d16f838974a6c15c7439695c8cb4601cbd2d; ttwid=1%7CKZnaIsRKXB01eDqrvBoT5-uSOcDVaLCCuvRQ93m64yU%7C1755538247%7C4811d460790d760a2d4ce894c0a2706914a35719b735514d405cc77605f0921d; tiktok_webapp_theme_source=light; tiktok_webapp_theme=light; msToken=1H1kg4j2hLjBMFJCezCIBO_osoivpLlbx977rWN2P68dod1Gp_lDJa6No_baAuaylllCy9xBpAHO5N_PI3_NnZb39RoEOIuh8hhtYtxkjlhX7-ffNAihbLH7SHzULgDUpgyMmN0VsT6f_ZpjYolqZscYxw==; msToken=QtwPZnGmwQrVVq0QCPx6BTzOq7FiUgBmMG7k7hyN_DAYrBAyZFuV1rNQsQqcqhlFltP-wh8mZFe4AnXzhdKRKrQHComnrbaqsuqrySTN2X9GfzN_7g1hnLjwFBEizPbUpjbAOfRmBGBcRWovddCCdLwWoQ==",
                "target_user_id": "7510342465174782984",
            }
        }

# Create a common response model
class ResponseModel(BaseModel):
    code: int = Field(default=200, description="HTTP status code")
    params: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="The parameters used in the request ",
    )
    data: Optional[Any] = Field(description="The response data")

    metadata: Optional[dict] = Field(
        default_factory=dict, description="The continuation metadata"
    )

    version: str = Field(
        default="0.0.1",
        description="The version of the API",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "params": {"query": "example"},
                "data": {"key": "value"},
                "version": "0.0.1",
            }
        }


#  Define an error response model
class ErrorResponseModel(BaseModel):
    code: int = Field(default=400, description="HTTP status code")
    message: str = Field(
        default="An error occurred. ",
        description="Error message ",
    )
    time: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="The time the error occurred ",
    )
    params: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="The parameters used in the request",
    )
    version: str = Field(
        default="0.0.1",
        description="The version of the API",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code": 400,
                "message": "Invalid request parameters.",
                "time": "2025-10-27 14:30:00",
                "params": {"param1": "invalid"},
                "version": "0.0.1",
            }
        }
