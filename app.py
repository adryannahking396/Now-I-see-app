import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import colorsys
import json

from streamlit_image_coordinates import streamlit_image_coordinates


# ============================================================
# NOW I SEE
# ============================================================

st.set_page_config(
    page_title="Now I See — Color Accessibility Tool",
    page_icon="images/star.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "image": None,
    "image_bytes": None,
    "palette": [],
    "selected_color": None,
    "selected_index": None,
    "custom_names": {},
    "deficiency": "Normal vision",
    "page": "Sample colors",
    "search_text": "",
    "search_active": False,
    "rename_mode": False,
    "last_click_time": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# OPTIONS
# ============================================================

DEFICIENCIES = [
    "Normal vision",
    "Protanopia (red blindness)",
    "Protanomaly (red weakness)",
    "Deuteranopia (green blindness)",
    "Deuteranomaly (green weakness)",
    "Tritanopia (blue blindness)",
    "Tritanomaly (blue weakness)",
    "Achromatopsia (no color vision)",
    "Achromatomaly (reduced color vision)",
]

DEFAULT_SELECTED_PURPLE = (61, 38, 82)  # dark purple default

COLOR_WORDS = {
    "red": (220, 55, 55),
    "orange": (235, 135, 45),
    "yellow": (235, 205, 75),
    "green": (65, 160, 90),
    "cyan": (65, 175, 175),
    "blue": (55, 105, 175),
    "purple": (125, 75, 185),
    "pink": (220, 105, 165),
    "magenta": (205, 60, 165),
    "brown": (130, 80, 50),
    "beige": (210, 180, 135),
    "gray": (130, 130, 130),
    "grey": (130, 130, 130),
    "black": (20, 20, 25),
    "white": (245, 245, 245),
}


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* PAGE */
    .stApp {
        background: #e7bff7;
    }

    [data-testid="stHeader"] {
        background: #151720;
        height: 60px;
    }

    [data-testid="stHeader"] * {
        color: white !important;
    }

    .main .block-container {
        max-width: 1210px;
        padding-top: 25px;
        padding-bottom: 40px;
        padding-left: 38px;
        padding-right: 38px;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #b979df;
        min-width: 140px;
        max-width: 140px;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding: 13px 8px 20px 8px;
    }

    [data-testid="stSidebar"] * {
        color: #281039;
    }

    .logo {
        text-align: center;
        margin: 15px 0 30px 0;
        line-height: 1;
    }

    .logo-star {
        font-size: 100px;
        font-weight: 900;
    }

    .logo-title {
        font-size: 15px;
        font-weight: 900;
        letter-spacing: 1px;
        margin-top: 5px;
    }

    .logo-sub {
        font-size: 15px;
        margin-top: 3px;
    }

    .side-heading {
        font-size: 5px !important;
        font-weight: 900;
        letter-spacing: 1px;
        color: #71378e !important;
        margin: 0 0 5px 2px;
        text-transform: uppercase;
    }

    [data-testid="stSidebar"] div.stButton > button {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        color: #281039 !important;
        text-align: left !important;
        font-size: 8px !important;
        min-height: 30px;
        padding: 3px 4px;
        border-radius: 6px;
        white-space: normal;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background: rgba(255,255,255,.35) !important;
    }

    /* TOP BAR */
    .top-line {
        display: flex;
        align-items: center;
        gap: 3px;
        margin-bottom: 38px;
    }

    .brand {
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 1.7px;
        color: #24162d;
    }

    .crumb {
        font-size: 7px;
        color: #76557f;
    }

    /* BUTTONS */
    div.stButton > button,
    div.stDownloadButton > button {
        border: 1px solid #b06bd5;
        background: #f0dafa;
        color: #31113e;
        border-radius: 7px;
        font-size: 8px;
        font-weight: 750;
        min-height: 29px;
        padding: 3px 9px;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        border-color: #6d2b8d;
        background: #f7eaff;
        color: #281030;
    }

    /* TOP IMPORT/EXPORT */
    .top-action div.stButton > button,
    .top-action div.stDownloadButton > button {
        background: #161923;
        color: white;
        border: 0;
        min-height: 34px;
        font-size: 8px;
    }

    /* UPLOADER */
    [data-testid="stFileUploader"] {
        background: #f4e4fa;
        border-radius: 7px;
        padding: 7px;
    }

    [data-testid="stFileUploader"] * {
        font-size: 8px !important;
    }

    /* EMPTY / IMAGE */
    .image-frame {
        background: #f7edfa;
        border: 1px dashed #ad6dcc;
        border-radius: 8px;
        padding: 8px;
    }

    .empty-frame {
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        flex-direction: column;
        color: #563568;
    }

    .empty-star {
        font-size: 38px;
        color: #70429a;
        margin-bottom: 14px;
    }

    .empty-title {
        font-size: 17px;
        font-weight: 800;
        color: #392054;
    }

    .empty-text {
        font-size: 9px;
        margin-top: 10px;
        color: #8a6099;
    }

    .image-label {
        font-size: 6px;
        color: #f4e9fa;
        background: #161923;
        display: inline-block;
        padding: 3px 6px;
        border-radius: 3px;
        margin-bottom: 4px;
        font-weight: 800;
    }

    .image-help {
        font-size: 7px;
        color: #704080;
        margin-top: 4px;
    }

    /* RIGHT PANEL */
    .color-panel {
        background: #b979df;
        min-height: 320px;
        padding: 9px;
        border-radius: 0;
    }

    .panel-title {
        font-size: 15px;
        font-weight: 850;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .color-preview {
        width: 100%;
        height: 48px;
        border-radius: 5px;
        margin-bottom: 7px;
    }

    .color-name {
        font-size: 12px;
        font-weight: 750;
        color: #ffffff;
        margin-bottom: 7px;
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        gap: 5px;
        padding: 4px 0;
        border-bottom: 1px solid rgba(255,255,255,.18);
        font-size: 10px;
        color: #eadcf1;
    }

    .info-row b {
        color: #ffffff;
    }

    .panel-label {
        font-size: 10px;
        color: #f0dff6;
        font-weight: 850;
        margin: 7px 0 3px 0;
        text-transform: uppercase;
    }

    /* PALETTE */
    .palette-heading {
        font-size: 6px;
        color: #7a3c96;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 15px;
    }

    .palette-title {
        font-size: 8px;
        font-weight: 850;
        color: #2d1835;
        margin-bottom: 6px;
    }

    .palette-card {
        background: #f7f2f8;
        border-radius: 5px;
        padding: 4px;
        min-height: 50px;
        border: 1px solid rgba(70,30,90,.08);
    }

    .palette-swatch {
        height: 18px;
        border-radius: 3px;
        margin-bottom: 3px;
    }

    .palette-name {
        font-size: 6px;
        font-weight: 800;
        color: #3d2944;
    }

    .palette-hex {
        font-size: 5px;
        color: #967d9d;
    }

    /* SEARCH */
    .search-result {
        background: rgba(255,255,255,.35);
        border-radius: 5px;
        padding: 5px;
        font-size: 7px;
        color: #3f194d;
        margin-top: 5px;
    }

    /* HIDE DEFAULT STREAMLIT CHROME */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COLOR FUNCTIONS
# ============================================================

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*[int(x) for x in rgb])


def rgb_to_hsl(rgb):
    r, g, b = [int(x) / 255 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(h * 360), round(s * 100), round(l * 100)


def color_name(rgb):
    r, g, b = [int(x) for x in rgb]

    if max(r, g, b) < 35:
        return "Black"

    if min(r, g, b) > 235:
        return "White"

    h, l, s = colorsys.rgb_to_hls(
        r / 255,
        g / 255,
        b / 255
    )

    h *= 360
    s *= 100

    if s < 12:
        return "Gray"

    if h < 15 or h >= 345:
        return "Red"
    if h < 45:
        return "Orange"
    if h < 70:
        return "Yellow"
    if h < 165:
        return "Green"
    if h < 195:
        return "Cyan"
    if h < 250:
        return "Blue"
    if h < 290:
        return "Purple"

    return "Pink"


def make_palette(image, number_of_colors=12):
    """
    Creates representative colors from the image.
    A normal photo can contain millions of slightly different
    RGB values, so the palette displays the main/distinct tones.
    """
    small = cv2.resize(
        image,
        (150, 150),
        interpolation=cv2.INTER_AREA
    )

    pixels = small.reshape((-1, 3)).astype(np.float32)

    criteria = (
        cv2.TERM_CRITERIA_EPS +
        cv2.TERM_CRITERIA_MAX_ITER,
        30,
        0.7
    )

    _, labels, centers = cv2.kmeans(
        pixels,
        number_of_colors,
        None,
        criteria,
        8,
        cv2.KMEANS_PP_CENTERS
    )

    counts = np.bincount(
        labels.flatten(),
        minlength=len(centers)
    )

    order = np.argsort(counts)[::-1]

    result = []

    for i in order:
        rgb = tuple(
            np.clip(
                np.round(centers[i]),
                0,
                255
            ).astype(int)
        )

        result.append(rgb)

    return result


def nearest_palette_color(rgb):
    if not st.session_state.palette:
        return None

    arr = np.array(
        st.session_state.palette,
        dtype=np.float32
    )

    target = np.array(
        rgb,
        dtype=np.float32
    )

    distances = np.linalg.norm(
        arr - target,
        axis=1
    )

    return int(np.argmin(distances))


def find_color(text):
    text = text.strip().lower()

    if not text:
        return None

    # HEX search
    if text.startswith("#") and len(text) == 7:
        try:
            return tuple(
                int(text[i:i+2], 16)
                for i in (1, 3, 5)
            )
        except ValueError:
            return None

    # Built-in color names take priority.
    if text in COLOR_WORDS:
        return COLOR_WORDS[text]

    # Custom names / palette names.
    for i, rgb in enumerate(st.session_state.palette):
        name = st.session_state.custom_names.get(
            str(i),
            color_name(rgb)
        )

        if text == name.lower():
            return tuple(int(x) for x in rgb)

    return None


def highlight_color(image, target, search_name="", tolerance=75):
    # Work from the original RGB image so searching is consistent
    # even when a color-vision simulation is selected.
    target = np.array(target, dtype=np.float32)
    name = search_name.strip().lower()

    if name in COLOR_WORDS:
        # For named colors use HSV hue matching. This catches
        # different shades of the requested color.
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        target_rgb = np.uint8([[target]])
        target_hsv = cv2.cvtColor(
            target_rgb,
            cv2.COLOR_RGB2HSV
        )[0][0]

        target_hue = int(target_hsv[0])
        hue_width = 15

        lower_hue = (target_hue - hue_width) % 180
        upper_hue = (target_hue + hue_width) % 180

        hue = hsv[:, :, 0]
        saturation = hsv[:, :, 1]
        value = hsv[:, :, 2]

        if lower_hue <= upper_hue:
            hue_match = (hue >= lower_hue) & (hue <= upper_hue)
        else:
            hue_match = (hue >= lower_hue) | (hue <= upper_hue)

        mask = (
            hue_match
            & (saturation >= 40)
            & (value >= 30)
        )
    else:
        image_float = image.astype(np.float32)
        distance = np.linalg.norm(
            image_float - target,
            axis=2
        )
        mask = distance <= tolerance

    result = (image.astype(np.float32) * 0.18).astype(np.uint8)
    result[mask] = image[mask]

    edges = cv2.Canny(
        mask.astype(np.uint8) * 255,
        50,
        150
    )

    result[edges > 0] = [255, 235, 40]

    return result, mask

# ============================================================
# COLOR VISION SIMULATION
# ============================================================

def protanopia(image):
    matrix = np.array([
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758],
    ])

    return np.clip(
        image @ matrix.T,
        0,
        255
    ).astype(np.uint8)


def deuteranopia(image):
    matrix = np.array([
        [0.625, 0.375, 0.000],
        [0.700, 0.300, 0.000],
        [0.000, 0.300, 0.700],
    ])

    return np.clip(
        image @ matrix.T,
        0,
        255
    ).astype(np.uint8)


def tritanopia(image):
    matrix = np.array([
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525],
    ])

    return np.clip(
        image @ matrix.T,
        0,
        255
    ).astype(np.uint8)


def simulate(image, deficiency):
    if deficiency == "Normal vision":
        return image

    if deficiency == "Protanopia (red blindness)":
        return protanopia(image)

    if deficiency == "Protanomaly (red weakness)":
        return cv2.addWeighted(
            image, 0.5,
            protanopia(image), 0.5, 0
        )

    if deficiency == "Deuteranopia (green blindness)":
        return deuteranopia(image)

    if deficiency == "Deuteranomaly (green weakness)":
        return cv2.addWeighted(
            image, 0.5,
            deuteranopia(image), 0.5, 0
        )

    if deficiency == "Tritanopia (blue blindness)":
        return tritanopia(image)

    if deficiency == "Tritanomaly (blue weakness)":
        return cv2.addWeighted(
            image, 0.5,
            tritanopia(image), 0.5, 0
        )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    gray_rgb = cv2.cvtColor(
        gray,
        cv2.COLOR_GRAY2RGB
    )

    if deficiency == "Achromatopsia (no color vision)":
        return gray_rgb

    if deficiency == "Achromatomaly (reduced color vision)":
        return cv2.addWeighted(
            image, 0.5,
            gray_rgb, 0.5, 0
        )

    return image


def reset_session():
    for key in DEFAULTS:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()


def load_image(uploaded):
    if uploaded is None:
        return

    image_bytes = uploaded.getvalue()

    if image_bytes == st.session_state.image_bytes:
        return

    image = Image.open(
        BytesIO(image_bytes)
    ).convert("RGB")

    image_array = np.array(image)

    st.session_state.image = image_array
    st.session_state.image_bytes = image_bytes
    st.session_state.palette = make_palette(
        image_array,
        12
    )
    st.session_state.selected_color = None
    st.session_state.selected_index = None
    st.session_state.custom_names = {}
    st.session_state.search_text = ""
    st.session_state.search_active = False
    st.session_state.page = "Sample colors"
    st.session_state.last_click_time = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo">
            <div class="logo-star">☆</div>
            <div class="logo-title">NOW I SEE</div>
            <div class="logo-sub">COLOR VISION</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-heading">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "🎨  Sample colors",
        key="nav_sample",
        width="stretch"
    ):
        st.session_state.page = "Sample colors"

    if st.button(
        "▣  My palettes",
        key="nav_palette",
        width="stretch"
    ):
        st.session_state.page = "My palettes"

    if st.button(
        "◐  Compare layers",
        key="nav_compare",
        width="stretch"
    ):
        st.session_state.page = "Compare layers"

    st.markdown(
        '<div class="side-heading" style="margin-top:14px;">SOURCE</div>',
        unsafe_allow_html=True
    )

    # THIS IS A REAL WORKING UPLOAD BUTTON IN THE SIDEBAR.
    sidebar_upload = st.file_uploader(
        "Open image",
        type=["png", "jpg", "jpeg", "webp"],
        key="sidebar_upload",
        label_visibility="visible"
    )

    load_image(sidebar_upload)

    if st.button(
        "↻  Reset session",
        key="nav_reset",
        width="stretch"
    ):
        reset_session()


# ============================================================
# TOP BAR
# ============================================================

brand_col, import_col, export_col, menu_col = st.columns(
    [7.0, 1.35, 1.35, .4],
    gap="small"
)

with brand_col:
    st.markdown(
        """
        <div class="top-line">
            <span class="brand">NOW I SEE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with import_col:
    st.markdown('<div class="top-action">', unsafe_allow_html=True)

    with st.popover("↥ Import source", use_container_width=True):
        top_upload = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="top_upload",
            label_visibility="visible"
        )

        if top_upload is not None:
            load_image(top_upload)

    st.markdown("</div>", unsafe_allow_html=True)

with export_col:
    st.markdown('<div class="top-action">', unsafe_allow_html=True)

    if st.session_state.palette:

        export_data = []

        for i, rgb in enumerate(
            st.session_state.palette
        ):
            export_data.append({
                "name": st.session_state.custom_names.get(
                    str(i),
                    color_name(rgb)
                ),
                "hex": rgb_to_hex(rgb),
                "rgb": [int(value) for value in rgb],
            })

        st.download_button(
            "↥ Export palette",
            data=json.dumps(
                export_data,
                indent=2
            ),
            file_name="now_i_see_palette.json",
            mime="application/json",
            width="stretch"
        )

    else:
        st.button(
            "↥ Export palette",
            disabled=True,
            width="stretch"
        )

    st.markdown("</div>", unsafe_allow_html=True)

with menu_col:
    with st.popover("•••"):
        st.write("👁️❤️🐑Peepaw!")
        st.caption(
            "-Love Addie Bug"
        )


# ============================================================
# MAIN IMAGE / RIGHT PANEL
# ============================================================

if st.session_state.image is not None:

    original = st.session_state.image

    # Apply color vision simulation first.
    displayed_image = simulate(
        original,
        st.session_state.deficiency
    )

    # Then apply search highlighting.
    found_color = None
    match_count = 0

    if (
        st.session_state.search_active
        and st.session_state.search_text.strip()
    ):

        found_color = find_color(
            st.session_state.search_text
        )

        if found_color is not None:

            displayed_image, mask = highlight_color(
                original,
                found_color,
                st.session_state.search_text
            )

            match_count = int(
                np.sum(mask)
            )

    left, right = st.columns(
        [7.1, 2.0],
        gap="small"
    )

    # --------------------------------------------------------
    # LEFT
    # --------------------------------------------------------

    with left:

        st.markdown(
            """
            <div class="hero-title">
                Capture the whole field,<br>
                not just one pixel.
            </div>
            """,
            unsafe_allow_html=True
        )

        h, w = displayed_image.shape[:2]

        # Keep the image close to the screenshot's proportions.
        max_width = 900

        if w > max_width:

            shown_h = int(
                h * max_width / w
            )

            shown = cv2.resize(
                displayed_image,
                (max_width, shown_h),
                interpolation=cv2.INTER_AREA
            )

        else:
            shown = displayed_image

        st.markdown(
            '<div class="image-label">IMAGE • COLOR SAMPLE</div>',
            unsafe_allow_html=True
        )

        # The component returns x/y plus the actual rendered image size.
        # Using those returned dimensions makes the sampled pixel line up
        # with the image even when Streamlit scales the component.
        shown_height, shown_width = shown.shape[:2]

        clicked = streamlit_image_coordinates(
            Image.fromarray(shown),
            width=shown_width,
            height=shown_height,
            key="clickable_image"
        )

        if clicked is not None:

            click_time = clicked.get(
                "unix_time"
            )

            # Only react to a brand-new click. This prevents the same
            # coordinate from being processed repeatedly after reruns.
            if click_time != st.session_state.last_click_time:

                st.session_state.last_click_time = click_time

                rendered_width = int(
                    clicked.get("width", shown_width)
                )
                rendered_height = int(
                    clicked.get("height", shown_height)
                )

                rendered_width = max(
                    1, rendered_width
                )
                rendered_height = max(
                    1, rendered_height
                )

                x = int(
                    clicked["x"]
                    * original.shape[1]
                    / rendered_width
                )

                y = int(
                    clicked["y"]
                    * original.shape[0]
                    / rendered_height
                )

                x = max(
                    0,
                    min(original.shape[1] - 1, x)
                )

                y = max(
                    0,
                    min(original.shape[0] - 1, y)
                )

                selected = tuple(
                    int(value)
                    for value in original[y, x]
                )

                st.session_state.selected_color = selected
                st.session_state.selected_index = nearest_palette_color(
                    selected
                )
                st.session_state.search_active = False
                st.session_state.search_text = ""

                st.rerun()

        st.markdown(
            '<div class="image-help">✦ Add another color anywhere</div>',
            unsafe_allow_html=True
        )

        if found_color is not None:

            total_pixels = (
                original.shape[0]
                * original.shape[1]
            )

            percent = (
                match_count /
                total_pixels *
                100
            )

            st.markdown(
                f"""
                <div class="search-result">
                    🔎 <b>{st.session_state.search_text}</b>
                    • {percent:.1f}% of the image matches
                </div>
                """,
                unsafe_allow_html=True
            )

        elif (
            st.session_state.search_active
            and st.session_state.search_text
        ):

            st.markdown(
                """
                <div class="search-result">
                    No matching color was found.
                    Try a color name such as orange, blue, green,
                    purple, red, or a HEX value.
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # RIGHT PANEL
    # --------------------------------------------------------

    with right:

        selected = st.session_state.selected_color

        if selected is None:

            preview = rgb_to_hex(DEFAULT_SELECTED_PURPLE)
            selected_name = "Dark purple"
            hex_value = "—"
            rgb_value = "—"
            hsl_value = "—"

        else:

            selected = tuple(
                map(int, selected)
            )

            preview = rgb_to_hex(selected)

            index = nearest_palette_color(
                selected
            )

            selected_name = color_name(
                selected
            )

            if index is not None:

                selected_name = (
                    st.session_state.custom_names.get(
                        str(index),
                        selected_name
                    )
                )

            hex_value = rgb_to_hex(
                selected
            )

            rgb_value = (
                f"rgb({selected[0]}, "
                f"{selected[1]}, "
                f"{selected[2]})"
            )

            hsl = rgb_to_hsl(selected)

            hsl_value = (
                f"hsl({hsl[0]}°, "
                f"{hsl[1]}%, "
                f"{hsl[2]}%)"
            )

        st.markdown(
            '<div class="color-panel">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-title">SELECTED COLOR</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="color-preview"
                 style="background:{preview};">
            </div>

            <div class="color-name">
                {selected_name}
            </div>

            <div class="info-row">
                <b>HEX</b>
                <span>{hex_value}</span>
            </div>

            <div class="info-row">
                <b>RGB</b>
                <span>{rgb_value}</span>
            </div>

            <div class="info-row">
                <b>HSL</b>
                <span>{hsl_value}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-label">Color vision</div>',
            unsafe_allow_html=True
        )

        st.session_state.deficiency = st.selectbox(
            "Color deficiency",
            DEFICIENCIES,
            index=DEFICIENCIES.index(
                st.session_state.deficiency
            ),
            key="deficiency_select",
            label_visibility="collapsed"
        )

        # SEARCH IS DIRECTLY BELOW THE DROPDOWN.
        st.markdown(
            '<div class="panel-label">Search for a color</div>',
            unsafe_allow_html=True
        )

        search = st.text_input(
            "Search",
            value=st.session_state.search_text,
            placeholder="Search...",
            key="search_box",
            label_visibility="collapsed"
        )

        search_button_col, clear_search_col = st.columns(2)

        with search_button_col:

            if st.button(
                "🔎 Find color",
                key="find_color_button",
                width="stretch"
            ):
                found = find_color(search)

                st.session_state.search_text = search
                st.session_state.search_active = True

                if found is not None:
                    st.session_state.selected_color = tuple(
                        int(x) for x in found
                    )
                    st.session_state.selected_index = (
                        nearest_palette_color(found)
                    )
                else:
                    st.session_state.selected_color = None
                    st.session_state.selected_index = None

                st.rerun()

        with clear_search_col:

            if st.button(
                "Clear",
                key="clear_search_button",
                width="stretch"
            ):
                st.session_state.search_text = ""
                st.session_state.search_active = False
                st.rerun()

        st.markdown("")

        rename_col, copy_col = st.columns(2)

        with rename_col:

            if st.button(
                "Rename",
                key="rename_button",
                disabled=(selected is None),
                width="stretch"
            ):
                st.session_state.rename_mode = True

        with copy_col:

            if st.button(
                "Copy HEX",
                key="copy_button",
                disabled=(selected is None),
                width="stretch"
            ):
                st.code(
                    hex_value,
                    language=None
                )
                st.caption(
                    "Select/copy the HEX value above."
                )

        if (
            st.session_state.rename_mode
            and selected is not None
        ):

            index = nearest_palette_color(
                selected
            )

            current_name = color_name(
                selected
            )

            if index is not None:
                current_name = (
                    st.session_state.custom_names.get(
                        str(index),
                        current_name
                    )
                )

            new_name = st.text_input(
                "New color name",
                value=current_name,
                key="new_color_name"
            )

            if st.button(
                "Save name",
                key="save_name",
                width="stretch"
            ):

                if index is not None:
                    st.session_state.custom_names[
                        str(index)
                    ] = new_name

                st.session_state.rename_mode = False
                st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# NO IMAGE YET
# ============================================================

else:

    left, right = st.columns(
        [7.1, 2.0],
        gap="small"
    )

    with left:

        st.markdown(
            """
            <div style="height:5px;"></div>
            <div class="image-frame">
                <div class="empty-frame">
                    <div class="empty-star">☆</div>
                    <div class="empty-title">
                        Choose an image to begin
                    </div>
                    <div class="empty-text">
                        Use Import source above or Open image
                        on the left to start exploring its colors.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        st.markdown(
            """
            <div class="color-panel">
                <div class="panel-title">SELECTED COLOR</div>
                <div class="color-preview"
                     style="background:#3D2652;">
                </div>
                <div class="color-name">
                    Dark purple
                </div>
                <div class="info-row">
                    <b>HEX</b>
                    <span>—</span>
                </div>
                <div class="info-row">
                    <b>RGB</b>
                    <span>—</span>
                </div>
                <div class="info-row">
                    <b>HSL</b>
                    <span>—</span>
                </div>
                <div class="panel-label">Color vision</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.deficiency = st.selectbox(
            "Color deficiency",
            DEFICIENCIES,
            index=DEFICIENCIES.index(
                st.session_state.deficiency
            ),
            key="empty_deficiency_select"
        )

        st.markdown(
            '<div class="panel-label">Search for a color</div>',
            unsafe_allow_html=True
        )

        st.text_input(
            "Search",
            placeholder="Search...",
            key="empty_search",
            label_visibility="collapsed"
        )


# ============================================================
# PALETTE SECTION
# ============================================================

st.markdown(
    '<div class="palette-heading">PALETTE / COLORS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="palette-title">Captured tones</div>',
    unsafe_allow_html=True
)

palette = st.session_state.palette

if not palette:

    st.caption(
        "Your image colors will appear here after you upload an image."
    )

else:

    # Six cards per row like the reference.
    number_of_columns = min(6, len(palette))

    palette_cols = st.columns(
        number_of_columns,
        gap="small"
    )

    for i, rgb in enumerate(palette):

        name = st.session_state.custom_names.get(
            str(i),
            color_name(rgb)
        )

        hex_value = rgb_to_hex(rgb)

        with palette_cols[
            i % number_of_columns
        ]:

            st.markdown(
                f"""
                <div class="palette-card">
                    <div class="palette-swatch"
                         style="background:{hex_value};">
                    </div>
                    <div class="palette-name">{name}</div>
                    <div class="palette-hex">{hex_value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Select",
                key=f"palette_select_{i}",
                width="stretch"
            ):

                st.session_state.selected_color = rgb
                st.session_state.selected_index = i
                st.session_state.search_active = False
                st.rerun()

    st.markdown("")

    clear_col, blank_col = st.columns(
        [1.25, 7]
    )

    with clear_col:

        if st.button(
            "Clear colors",
            key="clear_selected_color",
            width="stretch"
        ):

            index = st.session_state.selected_index

            if (
                index is not None
                and 0 <= index < len(
                    st.session_state.palette
                )
            ):

                # Remove only the selected palette color.
                st.session_state.palette.pop(index)

                new_names = {}

                for key, name in (
                    st.session_state.custom_names.items()
                ):

                    old_index = int(key)

                    if old_index < index:
                        new_names[str(old_index)] = name

                    elif old_index > index:
                        new_names[
                            str(old_index - 1
                            )
                        ] = name

                st.session_state.custom_names = new_names
                st.session_state.selected_color = None
                st.session_state.selected_index = None
                st.rerun()

            else:
                # If nothing is selected, make the button useful by
                # clearing the entire captured palette.
                st.session_state.palette = []
                st.session_state.custom_names = {}
                st.session_state.selected_color = None
                st.session_state.selected_index = None
                st.rerun()


# ============================================================
# EXTRA PAGES
# ============================================================

if st.session_state.page == "My palettes":

    st.markdown(
        "### My palettes"
    )

    if st.session_state.palette:
        st.write(
            "Your current captured tones are shown above. "
            "Use Export palette to save them."
        )
    else:
        st.info(
            "Upload an image to create a palette."
        )


if st.session_state.page == "Compare layers":

    st.markdown(
        "### Compare layers"
    )

    if st.session_state.image is None:

        st.info(
            "Upload an image first."
        )

    else:

        compare_left, compare_right = st.columns(2)

        with compare_left:
            st.markdown("**Original**")
            st.image(
                st.session_state.image,
                width="stretch"
            )

        with compare_right:
            st.markdown(
                f"**{st.session_state.deficiency}**"
            )

            st.image(
                simulate(
                    st.session_state.image,
                    st.session_state.deficiency
                ),
                width="stretch"
            )
