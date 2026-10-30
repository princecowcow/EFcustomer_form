"""客戶填單收集表（獨立版，公網畀客戶用）

客戶逐欄填 -> 多個型號撳「➕ 加型號」-> 撳「生成」-> copy 標準文字發返我哋。
唔接 token、唔寫文檔、唔使 login，安全。
"""
import streamlit as st
from datetime import date

INOUT_OPTIONS = ["收貨", "送貨", "自提", "提貨", "轉倉(收)", "轉倉(出)",
                 "寄貨DHL", "寄貨FEDEX", "寄貨UPS", "順豐寄付", "順豐到付",
                 "收貨 FEDEX", "收貨 DHL", "收貨 UPS", "收貨 順豐", "收票"]


def main():
    st.set_page_config(page_title="信杰電子 · 客戶填單", layout="wide")
    st.title("📋 信杰電子 · 客戶填單")
    st.divider()

    dc1, dc2 = st.columns([2, 1])
    f_date_text = dc1.text_input("A. 日期（留空＝今天；可手打）", key="cf_date")
    f_date_pick = dc2.date_input("📅 揀日子（選用）", value=None, key="cf_datepick")
    f_date = f_date_text.strip()
    if not f_date and f_date_pick:
        f_date = f_date_pick.strftime("%Y%m%d")
    if not f_date:
        f_date = date.today().strftime("%Y%m%d")
    hc1, hc2, hc3 = st.columns([3.2, 1.1, 2.2])
    with hc1:
        ic1, ic2, ic3 = st.columns([2.6, 0.12, 0.9])
        f_comp = ic1.text_input("D. 公司", key="cf_company")
        ic2.markdown("<div style='height:2.45rem'></div><div style='text-align:center;font-size:1.15rem'>—</div>", unsafe_allow_html=True)
        f_seq = ic3.text_input("流水號", placeholder="例 1", key="cf_seq")
    with hc2:
        f_inout = st.selectbox("F. 進出", [""] + INOUT_OPTIONS, key="cf_inout")
    with hc3:
        f_counter = st.text_input("G. 供應商(進)/出貨客戶", key="cf_counter")
    f_company = (f_comp.strip() + "-" + f_seq.strip()) if (f_comp.strip() and f_seq.strip()) else f_comp.strip()

    st.markdown("**型號資料（H/I/J/K 一組，幾多個型號就加幾組）**")
    if "cf_models" not in st.session_state:
        st.session_state["cf_models"] = [{"mpn": "", "qty": "", "remark": "", "awb": ""}]
    for i, m in enumerate(st.session_state["cf_models"]):
        mc1, mc2, mc3, mc4, mc5 = st.columns([3, 2, 3, 2, 1])
        m["mpn"] = mc1.text_input("H. 型号", value=m["mpn"], key=f"cf_mpn_{i}")
        m["qty"] = mc2.text_input("I. 數量 (出庫請用負號 : -500)", value=m["qty"], key=f"cf_qty_{i}")
        m["remark"] = mc3.text_input("J. 備註", value=m["remark"], key=f"cf_rem_{i}")
        m["awb"] = mc4.text_input("K. 入倉号/AWB", value=m["awb"], key=f"cf_awb_{i}")
        if mc5.button("🗑", key=f"cf_del_{i}"):
            st.session_state["cf_models"].pop(i)
            st.rerun()
    if st.button("➕ 加型號", key="cf_add"):
        st.session_state["cf_models"].append({"mpn": "", "qty": "", "remark": "", "awb": ""})
        st.rerun()

    if st.button("📋 生成標準格式文字", type="primary", key="cf_gen"):
        lines = [f"A. 日期 :{f_date}", f"D. 公司 :{f_company}"]
        if f_inout:
            lines.append(f"F. 進出 :{f_inout}")
        if f_counter:
            lines.append(f"G. 供應商(進)/出貨客戶 :{f_counter}")
        for m in st.session_state["cf_models"]:
            lines.append(f"H. 型号 :{m['mpn']}      I. 數量 :{m['qty']}")
            if m["remark"]:
                lines.append(f"J. 備註 :{m['remark']}")
            if m["awb"]:
                lines.append(f"K. 入倉号/AWB :{m['awb']}")
        st.session_state["cf_text"] = "\n".join(lines)

    if st.session_state.get("cf_text"):
        txt = st.session_state["cf_text"]
        st.code(txt, language="text")
        if st.button("📲 一鍵複製文字", key="cf_wechat"):
            import json as _json
            import streamlit.components.v1 as _components
            _payload = _json.dumps(txt, ensure_ascii=False)
            _components.html(
            "<script>const s=" + _payload + ";"
            "function _cp(){if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s);}"
            "else{const ta=document.createElement('textarea');ta.value=s;document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);}}"
            "_cp();document.body.innerHTML='<p><p>✅ 已複製，係微信比番我地就得</p>';"
            "</script>",
                height=60)
            st.caption("✅ 已複製，係微信比番我地就得")


if __name__ == "__main__":
    main()
