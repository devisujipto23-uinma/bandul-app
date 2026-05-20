import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =========================
# SETUP HALAMAN
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
# HALAMAN PERTAMA
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <style>

    .judul {
        text-align:center;
        font-size:50px;
        font-weight:bold;
        color:#0B5ED7;
        margin-top:20px;
    }

    .subjudul {
        text-align:center;
        font-size:20px;
        color:#444;
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
        '<div class="subjudul">Silakan isi data diri terlebih dahulu</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    nama = st.text_input("👤 Nama Lengkap")

    absen = st.text_input("🔢 Nomor Absen")

    kelas = st.text_input("🏫 Kelas")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # tombol mulai
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
# HALAMAN SIMULASI
# =========================
else:

    st.title("🔵 SIMULASI BANDUL MATEMATIS")

    st.write(f"""
    ### 👤 DATA SISWA
    - Nama : {st.session_state.nama}
    - Absen : {st.session_state.absen}
    - Kelas : {st.session_state.kelas}
    """)

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.header("⚙ Pengaturan")

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

    # =========================
    # TOMBOL
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        start = st.button("▶ START")

    with col2:
        stop = st.button("⏸ STOP")

    with col3:
        reset = st.button("🔄 RESET")

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
    st.subheader("📌 Rumus Bandul")

    st.latex(
        r"\theta(t)=\theta_0\cos\left(\sqrt{\frac{g}{L}}t\right)"
    )

    st.latex(
        r"T=2\pi\sqrt{\frac{L}{g}}"
    )

    # =========================
    # TEMPAT GRAFIK
    # =========================
    grafik = st.empty()

    info = st.empty()

    # =========================
    # PARAMETER
    # =========================
    theta0 = np.radians(sudut)

    omega = np.sqrt(g / L)

    dt = 0.05

    # =========================
    # SIMULASI BERJALAN
    # =========================
    if st.session_state.run:

        x_history = []

        y_history = []

        for i in range(1000):

            if not st.session_state.run:
                break

            t = i * dt

            # =========================
            # PERSAMAAN BANDUL
            # =========================
            theta = theta0 * np.cos(omega * t)

            x = L * np.sin(theta)

            y = -L * np.cos(theta)

            # jejak
            x_history.append(x)

            y_history.append(y)

            if len(x_history) > 100:
                x_history.pop(0)
                y_history.pop(0)

            # =========================
            # GELOMBANG
            # =========================
            wave_x = np.linspace(
                0,
                4*np.pi,
                500
            )

            wave_y = np.sin(
                wave_x - 3*t
            )

            # =========================
            # FIGURE
            # =========================
            fig, (ax1, ax2) = plt.subplots(
                2,
                1,
                figsize=(8,10)
            )

            # =========================
            # GRAFIK BANDUL
            # =========================
            ax1.set_title("Gerak Bandul")

            ax1.set_xlim(-L-1, L+1)

            ax1.set_ylim(-L-1, 1)

            ax1.set_aspect('equal')

            ax1.grid(True)

            # tali
            ax1.plot(
                [0, x],
                [0, y],
                linewidth=3
            )

            # bola
            ax1.plot(
                x,
                y,
                'o',
                markersize=20
            )

            # jejak
            ax1.plot(
                x_history,
                y_history,
                linewidth=2,
                alpha=0.5
            )

            # =========================
            # GRAFIK GELOMBANG
            # =========================
            ax2.set_title("Gelombang Bergerak")

            ax2.set_xlim(0, 4*np.pi)

            ax2.set_ylim(-1.5, 1.5)

            ax2.grid(True)

            ax2.plot(
                wave_x,
                wave_y,
                linewidth=2
            )

            # titik bergerak
            titik_x = t % (4*np.pi)

            titik_y = np.sin(
                titik_x - 3*t
            )

            ax2.scatter(
                titik_x,
                titik_y,
                s=100
            )

            # =========================
            # TAMPILKAN GRAFIK
            # =========================
            grafik.pyplot(
                fig,
                clear_figure=True
            )

            plt.close(fig)

            # =========================
            # DATA REALTIME
            # =========================
            periode = 2 * np.pi * np.sqrt(L/g)

            frekuensi = 1 / periode

            info.markdown(f"""
            ## 📊 DATA REAL-TIME

            - ⏱ Waktu : {t:.2f} s
            - 📍 Posisi X : {x:.2f} m
            - 📍 Posisi Y : {y:.2f} m
            - 📐 Sudut : {np.degrees(theta):.2f}°
            - 🔄 Periode : {periode:.2f} s
            - 🌊 Frekuensi : {frekuensi:.2f} Hz
            """)

            time.sleep(0.03)

    # =========================
    # TOMBOL KEMBALI
    # =========================
    if st.button("⬅ Kembali ke Halaman Awal"):

        st.session_state.page = "home"

        st.session_state.run = False

        st.rerun()