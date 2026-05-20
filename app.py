import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =====================================
# SETUP HALAMAN
# =====================================
st.set_page_config(
    page_title="Simulasi Bandul Matematis",
    layout="wide"
)

# =====================================
# SESSION STATE
# =====================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "run" not in st.session_state:
    st.session_state.run = False

if "t" not in st.session_state:
    st.session_state.t = 0.0

if "x_history" not in st.session_state:
    st.session_state.x_history = []

if "y_history" not in st.session_state:
    st.session_state.y_history = []

# =====================================
# HALAMAN AWAL
# =====================================
if st.session_state.page == "home":

    st.markdown("""
    <style>

    .judul {
        text-align:center;
        font-size:45px;
        font-weight:bold;
        color:#0B5ED7;
    }

    .subjudul {
        text-align:center;
        font-size:20px;
        color:gray;
        margin-bottom:30px;
    }

    .kotak {
        background: linear-gradient(135deg,#74ebd5,#ACB6E5);
        padding:35px;
        border-radius:20px;
        box-shadow:0px 5px 15px rgba(0,0,0,0.2);
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="judul">🔵 SIMULASI BANDUL MATEMATIS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subjudul">Isi data diri terlebih dahulu</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    nama = st.text_input("👤 Nama Lengkap")

    absen = st.text_input("🔢 Nomor Absen")

    kelas = st.text_input("🏫 Kelas")

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 MULAI SIMULASI"):

        if nama == "" or absen == "" or kelas == "":
            st.error("Harap isi semua data!")

        else:
            st.session_state.nama = nama
            st.session_state.absen = absen
            st.session_state.kelas = kelas
            st.session_state.page = "simulasi"

            st.rerun()

# =====================================
# HALAMAN SIMULASI
# =====================================
else:

    st.title("🔵 SIMULASI BANDUL MATEMATIS REAL-TIME")

    st.write(f"""
    ### 👤 DATA SISWA

    - Nama : {st.session_state.nama}
    - Absen : {st.session_state.absen}
    - Kelas : {st.session_state.kelas}
    """)

    # =====================================
    # SIDEBAR
    # =====================================
    st.sidebar.header("⚙ PARAMETER")

    L = st.sidebar.slider(
        "Panjang Tali (m)",
        1.0,
        10.0,
        5.0
    )

    g = st.sidebar.slider(
        "Gravitasi (m/s²)",
        1.0,
        20.0,
        9.8
    )

    sudut = st.sidebar.slider(
        "Sudut Awal (°)",
        1,
        90,
        30
    )

    # =====================================
    # TOMBOL
    # =====================================
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶ START"):
            st.session_state.run = True

    with col2:
        if st.button("⏸ STOP"):
            st.session_state.run = False

    with col3:
        if st.button("🔄 RESET"):

            st.session_state.run = False

            st.session_state.t = 0.0

            st.session_state.x_history = []

            st.session_state.y_history = []

            st.rerun()

    # =====================================
    # RUMUS
    # =====================================
    st.subheader("📌 Rumus Bandul Matematis")

    st.latex(
        r"\theta(t)=\theta_0 \cos\left(\sqrt{\frac{g}{L}}t\right)"
    )

    st.latex(
        r"T=2\pi\sqrt{\frac{L}{g}}"
    )

    # =====================================
    # PLACEHOLDER
    # =====================================
    grafik = st.empty()

    data = st.empty()

    # =====================================
    # PERHITUNGAN
    # =====================================
    theta0 = np.radians(sudut)

    omega = np.sqrt(g / L)

    t = st.session_state.t

    theta = theta0 * np.cos(omega * t)

    x = L * np.sin(theta)

    y = -L * np.cos(theta)

    # =====================================
    # HISTORY
    # =====================================
    st.session_state.x_history.append(x)

    st.session_state.y_history.append(y)

    if len(st.session_state.x_history) > 50:
        st.session_state.x_history.pop(0)
        st.session_state.y_history.pop(0)

    # =====================================
    # GELOMBANG
    # =====================================
    wave_x = np.linspace(0, 4*np.pi, 300)

    wave_y = np.sin(wave_x - (2*t))

    # =====================================
    # FIGURE
    # =====================================
    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(8, 10)
    )

    # =====================================
    # BANDUL
    # =====================================
    ax1.set_title("Simulasi Bandul Matematis")

    ax1.set_xlim(-L-1, L+1)

    ax1.set_ylim(-L-1, 1)

    ax1.set_aspect("equal")

    ax1.grid()

    # tali
    ax1.plot([0, x], [0, y], lw=3)

    # bola
    ax1.plot(x, y, "o", markersize=18)

    # lintasan
    ax1.plot(
        st.session_state.x_history,
        st.session_state.y_history,
        alpha=0.5
    )

    # =====================================
    # GELOMBANG
    # =====================================
    ax2.set_title("Simulasi Gelombang")

    ax2.set_xlim(0, 4*np.pi)

    ax2.set_ylim(-1.5, 1.5)

    ax2.grid()

    ax2.plot(
        wave_x,
        wave_y,
        color="blue",
        linewidth=2
    )

    ax2.scatter(
        t % (4*np.pi),
        np.sin(t),
        s=100
    )

    # =====================================
    # TAMPILKAN
    # =====================================
    grafik.pyplot(fig)

    # =====================================
    # DATA REAL TIME
    # =====================================
    periode = 2 * np.pi * np.sqrt(L / g)

    frekuensi = 1 / periode

    data.markdown(f"""
    ## 📊 DATA REAL-TIME

    - ⏱ Waktu : {t:.2f} s
    - 📍 Posisi X : {x:.2f} m
    - 📍 Posisi Y : {y:.2f} m
    - 📐 Sudut : {np.degrees(theta):.2f}°
    - 🔄 Periode : {periode:.2f} s
    - 🌊 Frekuensi : {frekuensi:.2f} Hz
    """)

    # =====================================
    # UPDATE WAKTU
    # =====================================
    if st.session_state.run:

        st.session_state.t += 0.1

        time.sleep(0.05)

        st.rerun()

    # =====================================
    # KEMBALI
    # =====================================
    st.write("")

    if st.button("⬅ Kembali ke Halaman Awal"):

        st.session_state.page = "home"

        st.session_state.run = False

        st.session_state.t = 0.0

        st.rerun()