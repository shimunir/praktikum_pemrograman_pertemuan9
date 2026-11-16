# verifikasi.py
# Verifikasi hasil praktikum Pertemuan 9:
# memeriksa keberadaan 4 grafik (PNG) dan 2 berkas laporan (HTML, PDF).
#
# Path dihitung dari lokasi berkas ini, sehingga hasilnya sama di mana pun
# terminal dijalankan. Jika ada berkas yang belum ada, program akan
# menjalankan visualisasi_laporan.py lebih dulu untuk membuatnya.

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BERKAS = [
    ("grafik", "grafik_garis_tren.png"),
    ("grafik", "grafik_batang_lini.png"),
    ("grafik", "grafik_sebar_operator.png"),
    ("grafik", "histogram_jumlah.png"),
    ("laporan", "laporan_produksi.html"),
    ("laporan", "laporan_produksi.pdf"),
]


def ada(folder, nama):
    path = os.path.join(BASE, folder, nama)
    return os.path.isfile(path) and os.path.getsize(path) > 0


def pastikan_berkas_ada():
    """Bila ada berkas yang belum dibuat, jalankan program visualisasi."""
    if all(ada(f, n) for f, n in BERKAS):
        return
    print("Berkas hasil belum lengkap, menjalankan visualisasi_laporan.py ...\n")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import visualisasi_laporan
        visualisasi_laporan.main()
    except ModuleNotFoundError as e:
        print(f"\nPustaka belum terpasang: {e.name}")
        print(f"Jalankan: python -m pip install pandas matplotlib\n")
    except Exception as e:
        print(f"\nGagal membuat berkas: {e}\n")


def verifikasi():
    pastikan_berkas_ada()

    print("=" * 60)
    print("VERIFIKASI HASIL PRAKTIKUM PERTEMUAN 9")
    print("=" * 60)

    lulus = 0
    total = 0

    for folder, nama in BERKAS:
        total += 1
        ok = ada(folder, nama)
        if ok:
            lulus += 1
        print(f"  ../{folder}/{nama}: {'LULUS' if ok else 'GAGAL'}")

    print(f"\nTotal: {total} uji, Lulus: {lulus}, Gagal: {total - lulus}")
    print(f"Persentase kelulusan: {lulus / total * 100:.1f}%")


if __name__ == "__main__":
    verifikasi()
