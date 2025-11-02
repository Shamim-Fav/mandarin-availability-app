# Logo settings (use the URL you provided)
LOGO_URL = "https://github.com/Shamim-Fav/mandarin-availability-app/blob/main/logo.png"
LOCAL_LOGO = "logo.png"  # optional local fallback

def show_logo(url=LOGO_URL, local_fallback=LOCAL_LOGO, width=200):
    try:
        # Try st.image first (works for PNG/JPG and sometimes SVG)
        st.image(url, width=width)
    except Exception:
        # If st.image fails (common with SVGs), render raw HTML <img>
        try:
            st.markdown(f'<div style="text-align:center;"><img src="{url}" width="{width}"></div>',
                        unsafe_allow_html=True)
        except Exception:
            # Final fallback: try local file if present
            try:
                st.image(local_fallback, width=width)
            except Exception:
                # If everything fails, show a small text placeholder
                st.write("Mandarin Oriental")

# Show the logo (call this before the title)
show_logo()
st.title("Hong Kong – Mandarin Oriental Availability Checker")
st.info("This app checks room availability for **Hong Kong – Mandarin Oriental**")
