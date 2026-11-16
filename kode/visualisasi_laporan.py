# visualisasi_laporan.py
# Program visualisasi data dan laporan otomatis.
# Dibuat oleh: [Nama Mahasiswa] - [NIM]

import os
import sys
import subprocess
import shutil

import matplotlib
matplotlib.use("Agg")  # backend tanpa layar, aman dijalankan di terminal/server
import matplotlib.pyplot as plt
import pandas as pd

# Folder induk (Pertemuan_09), dihitung dari lokasi berkas ini sehingga
# program dapat dijalankan dari folder mana pun.
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def muat_data(nama_berkas: str) -> pd.DataFrame:
    """Memuat data dari berkas CSV."""
    return pd.read_csv(nama_berkas)


def buat_grafik_garis(df: pd.DataFrame, folder: str) -> str:
    """Membuat grafik garis tren total produksi harian."""
    total_harian = df.groupby("tanggal")["jumlah"].sum().reset_index()

    plt.figure(figsize=(8, 5))
    plt.plot(total_harian["tanggal"], total_harian["jumlah"],
             marker="o", color="steelblue", linewidth=2)
    plt.title("Tren Total Produksi Harian", fontsize=14)
    plt.xlabel("Tanggal", fontsize=12)
    plt.ylabel("Total Produksi (kg)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    path = os.path.join(folder, "grafik_garis_tren.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def buat_grafik_batang(df: pd.DataFrame, folder: str) -> str:
    """Membuat grafik batang total produksi per lini."""
    total_lini = df.groupby("liniproduksi")["jumlah"].sum().reset_index()

    plt.figure(figsize=(8, 5))
    plt.bar(total_lini["liniproduksi"], total_lini["jumlah"],
            color=["#4C72B0", "#DD8452"])
    plt.title("Total Produksi per Lini", fontsize=14)
    plt.xlabel("Lini Produksi", fontsize=12)
    plt.ylabel("Total Produksi (kg)", fontsize=12)
    for i, v in enumerate(total_lini["jumlah"]):
        plt.text(i, v + 5, str(v), ha="center", fontsize=10)
    plt.tight_layout()

    path = os.path.join(folder, "grafik_batang_lini.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def buat_grafik_sebar(df: pd.DataFrame, folder: str) -> str:
    """Membuat grafik sebar hubungan jumlah produksi dan operator."""
    # Agregasi: total produksi per operator
    per_operator = df.groupby("operator")["jumlah"].sum().reset_index()

    plt.figure(figsize=(8, 5))
    plt.scatter(per_operator["operator"], per_operator["jumlah"],
                color="crimson", s=100, alpha=0.7)
    plt.title("Sebaran Total Produksi per Operator", fontsize=14)
    plt.xlabel("Operator", fontsize=12)
    plt.ylabel("Total Produksi (kg)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    path = os.path.join(folder, "grafik_sebar_operator.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def buat_histogram(df: pd.DataFrame, folder: str) -> str:
    """Membuat histogram distribusi jumlah produksi."""
    plt.figure(figsize=(8, 5))
    plt.hist(df["jumlah"], bins=8, color="seagreen", edgecolor="black", alpha=0.75)
    plt.title("Distribusi Jumlah Produksi", fontsize=14)
    plt.xlabel("Jumlah Produksi (kg)", fontsize=12)
    plt.ylabel("Frekuensi", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    path = os.path.join(folder, "histogram_jumlah.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def buat_laporan_html(grafik: dict, ringkasan: pd.DataFrame, nama_berkas: str) -> None:
    """Menyusun laporan HTML yang menggabungkan grafik dan tabel ringkasan.

    Path gambar dibuat relatif terhadap lokasi berkas laporan agar gambar
    tampil di peramban (menghindari kesalahan E07).
    """
    folder_laporan = os.path.dirname(os.path.abspath(nama_berkas))
    rel = {k: os.path.relpath(os.path.abspath(v), folder_laporan).replace("\\", "/")
           for k, v in grafik.items()}

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Laporan Produksi</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
        th, td {{ border: 1px solid #bbb; padding: 8px; text-align: left; }}
        th {{ background-color: #ecf0f1; }}
        img {{ max-width: 100%; height: auto; margin-top: 10px; }}
        .footer {{ margin-top: 40px; font-size: 12px; color: #7f8c8d; }}
        @media print {{ h2 {{ page-break-after: avoid; }} img {{ page-break-inside: avoid; }} }}
    </style>
</head>
<body>
    <h1>Laporan Produksi Harian</h1>
    <p>Laporan ini dihasilkan secara otomatis oleh program Python.</p>

    <h2>1. Tren Total Produksi Harian</h2>
    <img src="{rel['garis']}" alt="Grafik Garis">

    <h2>2. Total Produksi per Lini</h2>
    <img src="{rel['batang']}" alt="Grafik Batang">

    <h2>3. Sebaran Total Produksi per Operator</h2>
    <img src="{rel['sebar']}" alt="Grafik Sebar">

    <h2>4. Distribusi Jumlah Produksi</h2>
    <img src="{rel['histogram']}" alt="Histogram">

    <h2>5. Ringkasan Data</h2>
    {ringkasan.to_html(index=False)}

    <div class="footer">
        <p>Dibuat otomatis pada: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
    with open(nama_berkas, mode="w", encoding="utf-8") as f:
        f.write(html)


def konversi_pdf(path_html: str, path_pdf: str) -> bool:
    """Mengonversi HTML ke PDF secara otomatis (tanpa penyuntingan manual).

    Mencoba berurutan: WeasyPrint -> Chrome/Chromium headless.
    Mengembalikan True bila PDF berhasil dibuat.
    """
    # 1) WeasyPrint (opsional)
    try:
        from weasyprint import HTML
        HTML(filename=path_html).write_pdf(path_pdf)
        return os.path.exists(path_pdf)
    except Exception:
        pass

    # 2) Chrome / Chromium / Edge headless
    kandidat = ["google-chrome", "chromium", "chromium-browser", "chrome",
                "msedge",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
    for k in kandidat:
        exe = shutil.which(k) or (k if os.path.exists(k) else None)
        if not exe:
            continue
        try:
            subprocess.run(
                [exe, "--headless", "--no-sandbox", "--disable-gpu",
                 "--no-pdf-header-footer",
                 f"--print-to-pdf={os.path.abspath(path_pdf)}",
                 "file:///" + os.path.abspath(path_html).replace("\\", "/").lstrip("/")],
                check=True, capture_output=True, timeout=120)
            if os.path.exists(path_pdf):
                return True
        except Exception:
            continue
    return False


def main():
    print("=" * 60)
    print("PROGRAM VISUALISASI DAN LAPORAN OTOMATIS")
    print("=" * 60)

    # 1. Muat data
    df = muat_data(os.path.join(BASE, "data", "data_produksi_bersih.csv"))
    print(f"Data dimuat: {len(df)} baris")

    # 2. Buat grafik
    folder_grafik = os.path.join(BASE, "grafik")
    os.makedirs(folder_grafik, exist_ok=True)

    grafik = {
        "garis": buat_grafik_garis(df, folder_grafik),
        "batang": buat_grafik_batang(df, folder_grafik),
        "sebar": buat_grafik_sebar(df, folder_grafik),
        "histogram": buat_histogram(df, folder_grafik),
    }
    print("Empat grafik berhasil dibuat:")
    for nama, path in grafik.items():
        print(f"  - {nama}: ../grafik/{os.path.basename(path)}")

    # 3. Ringkasan
    ringkasan = df.groupby("liniproduksi").agg(
        total_jumlah=("jumlah", "sum"),
        rata_rata=("jumlah", "mean"),
        maksimum=("jumlah", "max"),
        minimum=("jumlah", "min"),
    ).reset_index()

    # 4. Buat laporan HTML
    os.makedirs(os.path.join(BASE, "laporan"), exist_ok=True)
    path_laporan = os.path.join(BASE, "laporan", "laporan_produksi.html")
    buat_laporan_html(grafik, ringkasan, path_laporan)
    print("\nLaporan HTML disimpan ke: ../laporan/laporan_produksi.html")

    # 5. Konversi ke PDF otomatis
    path_pdf = os.path.join(BASE, "laporan", "laporan_produksi.pdf")
    if konversi_pdf(path_laporan, path_pdf):
        print("Laporan PDF disimpan ke: ../laporan/laporan_produksi.pdf")
    else:
        print("\nKonversi otomatis ke PDF gagal. Lakukan secara manual:")
        print("  1. Buka laporan HTML di peramban.")
        print("  2. Tekan Ctrl+P (Print).")
        print("  3. Pilih 'Save as PDF'.")
        print("  4. Simpan sebagai laporan_produksi.pdf.")


if __name__ == "__main__":
    main()
