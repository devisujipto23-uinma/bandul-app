import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =========================
# SETUP
# =========================
st.set_page_config(page_title="Bandul Mobile", layout="wide")

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

    st.title("🔵 SIMULASI BANDUL MATEMATIS")

    st.write("Isi data dulu sebelum mulai")

    nama = st.text_input("Nama")
    absen = st.text_input("Absen")
    kelas = st.text_input("Kelas")

    if st.button("🚀 MULAI"):

        if nama and absen and kelas:
            st.session_state.nama = nama
            st.session_state.absen = absen
            st.session_state.kelas = kelas
            st.session_state.page = "simulasi"
            st.rerun()
        else:
            st.error("Lengkapi semua data!")

# =========================
# HALAMAN 2
# =========================
else:

    st.title("📱 BANDUL REAL-TIME")

    st.success(f"Nama: {st.session_state.nama} | Kelas: {st.session_state.kelas}")

    # =========================
    # INPUT (TIDAK SIDEBAR LAGI)
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        L = st.slider("Panjang (m)", 1.0, 10.0, 5.0)

    with col2:
        g = st.slider("Gravitasi", 1.0, 20.0, 9.8)

    with col3:
        sudut = st.slider("Sudut (°)", 1, 90, 30)

    # =========================
    # BUTTON CONTROL (MOBILE FRIENDLY)
    # =========================
    colA, colB = st.columns(2)

    with colA:
        if st.button("▶ START"):
            st.session_state.run = True

    with colB:
        if st.button("⏸ STOP"):
            st.session_state.run = False

    st.divider()

    # =========================
    # PLACEHOLDER
    # =========================
    plot_area = st.empty()
    info_area = st.empty()

    # =========================
    # FISIKA
    # =========================
    theta0 = np.radians(sudut)
    omega = np.sqrt(g / L)

    t = 0
    dt = 0.1

    x_history = []
    y_history = []

    # =========================
    # LOOP REAL-TIME
    # =========================
    while st.session_state.run:

        theta = theta0 * np.cos(omega * t)

        x = L * np.sin(theta)
        y = -L * np.cos(theta)

        x_history.append(x)
        y_history.append(y)

        if len(x_history) > 50:
            x_history.pop(0)
            y_history.pop(0)

        fig, ax = plt.subplots()

        ax.set_xlim(-L-1, L+1)
        ax.set_ylim(-L-1, 1)
        ax.set_aspect("equal")

        ax.plot([0, x], [0, y], lw=3)
        ax.plot(x, y, "o", markersize=15)
        ax.plot(x_history, y_history, alpha=0.5)

        plot_area.pyplot(fig)

        periode = 2 * np.pi * np.sqrt(L / g)
        frekuensi = 1 / periode

        info_area.markdown(f"""
        ### 📊 DATA REAL-TIME
        - Waktu: {round(t,2)} s  
        - Posisi X: {x:.2f} m  
        - Periode: {periode:.2f} s  
        - Frekuensi: {frekuensi:.2f} Hz  
        """)

        t += dt
        time.sleep(0.05)

    if st.button("⬅ Kembali"):
        st.session_state.page = "home"
        st.session_state.run = False
        st.rerun()