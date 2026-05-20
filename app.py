import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =========================
# SETUP
# =========================
st.set_page_config(
    page_title="Simulasi Bandul Matematis",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "run" not in st.session_state:
    st.session_state.run = False

# =========================
# HALAMAN 1
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <style>

    .main {
        background-color: #f5f7fa;
    }

    .judul {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #0B5ED7;
        margin-bottom: 20px;
    }

    .subjudul {
        text-align: center;
        font-size: 20px;
        color: #444;
        margin-bottom: 30px;
    }

    .kotak {
        background: linear-gradient(135deg,#74ebd5,#ACB6E5);
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="judul">🔵 SIMULASI BANDUL MATEMATIS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subjudul">Silakan isi data diri sebelum memulai simulasi</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    nama = st.text_input("👤 Nama Lengkap")
    absen = st.text_input("🔢 Nomor Absen")
    kelas = st.text_input("🏫 Kelas")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 MULAI SIMULASI"):

        if nama == "" or absen == "" or kelas == "":
            st.error("Harap isi semua data terlebih dahulu!")
        else:
            st.session_state.nama = nama
            st.session_state.absen = absen
            st.session_state.kelas = kelas
            st.session_state.page = "simulasi"
            st.rerun()

# =========================
# HALAMAN 2
# =========================
else:

    st.title("🔵 SIMULASI BANDUL MATEMATIS REAL-TIME")

    st.write(f"""
    ### 👤 DATA SISWA
    - Nama : {st.session_state.nama}
    - Absen : {st.session_state.absen}
    - Kelas : {st.session_state.kelas}
    """)

    # =========================
    # SIDEBAR PARAMETER
    # =========================
    st.sidebar.header("⚙ PARAMETER FISIKA")

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

    start = st.sidebar.button("▶ START")

    stop = st.sidebar.button("⏸ STOP")

    reset = st.sidebar.button("🔄 RESET")

    if start:
        st.session_state.run = True

    if stop:
        st.session_state.run = False

    if reset:
        st.session_state.run = False
        st.rerun()

    # =========================
    # RUMUS
    # =========================
    st.subheader("📌 Rumus Bandul Matematis")

    st.latex(
        r"\theta(t)=\theta_0\cos\left(\sqrt{\frac{g}{L}}t\right)"
    )

    st.latex(
        r"T=2\pi\sqrt{\frac{L}{g}}"
    )

    # =========================
    # PLACEHOLDER
    # =========================
    plot_area = st.empty()

    info_area = st.empty()

    # =========================
    # PERHITUNGAN FISIKA
    # =========================
    theta0 = np.radians(sudut)

    omega = np.sqrt(g / L)

    t = 0

    dt = 0.1

    x_history = []

    y_history = []

    # =========================
    # LOOP SIMULASI
    # =========================
    while st.session_state.run:

        # -------------------------
        # Persamaan bandul
        # -------------------------
        theta = theta0 * np.cos(omega * t)

        x = L * np.sin(theta)

        y = -L * np.cos(theta)

        # -------------------------
        # Riwayat gerakan
        # -------------------------
        x_history.append(x)

        y_history.append(y)

        if len(x_history) > 50:
            x_history.pop(0)
            y_history.pop(0)

        # =========================
        # GELOMBANG
        # =========================
        wave_x = np.linspace(0, 4*np.pi, 300)

        wave_y = np.sin(wave_x - (2*t))

        # =========================
        # FIGURE
        # =========================
        fig, (ax1, ax2) = plt.subplots(
            2,
            1,
            figsize=(8, 10)
        )

        # =========================
        # BANDUL
        # =========================
        ax1.set_title("Simulasi Bandul Matematis")

        ax1.set_xlim(-L-1, L+1)

        ax1.set_ylim(-L-1, 1)

        ax1.set_aspect("equal")

        ax1.grid()

        # tali bandul
        ax1.plot([0, x], [0, y], lw=3)

        # bola bandul
        ax1.plot(x, y, "o", markersize=18)

        # jejak lintasan
        ax1.plot(
            x_history,
            y_history,
            alpha=0.5
        )

        # =========================
        # GELOMBANG BERGERAK
        # =========================
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

        # titik bergerak
        ax2.scatter(
            t % (4*np.pi),
            np.sin(t),
            s=100
        )

        # =========================
        # TAMPILKAN
        # =========================
        plot_area.pyplot(fig)

        # =========================
        # DATA REAL TIME
        # =========================
        periode = 2 * np.pi * np.sqrt(L / g)

        frekuensi = 1 / periode

        info_area.markdown(f"""
        ## 📊 DATA REAL-TIME

        - ⏱ Waktu : {round(t,2)} s
        - 📍 Posisi X : {x:.2f} m
        - 📍 Posisi Y : {y:.2f} m
        - 📐 Sudut : {np.degrees(theta):.2f}°
        - 🔄 Periode : {periode:.2f} s
        - 🌊 Frekuensi : {frekuensi:.2f} Hz
        """)

        # =========================
        # UPDATE WAKTU
        # =========================
        t += dt

        time.sleep(0.05)

    # =========================
    # TOMBOL KEMBALI
    # =========================
    if st.button("⬅ Kembali ke Halaman Awal"):

        st.session_state.page = "home"

        st.session_state.run = False

        st.rerun()