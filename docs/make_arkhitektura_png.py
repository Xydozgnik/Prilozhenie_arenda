# -*- coding: utf-8 -*-
"""Генерирует docs/server-arkhitektura.png — схему архитектуры сервера «Порога».
Запуск: python docs/make_arkhitektura_png.py (из корня репозитория)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(15, 10))
ax.set_xlim(0, 142)
ax.set_ylim(0, 96)
ax.axis("off")
fig.patch.set_facecolor("white")

TXT = "#2E3B2E"

def group(x, y, w, h, label, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=2",
                                fc=fc, ec=ec, lw=1.6, alpha=0.45, zorder=1))
    ax.text(x + 2, y + h - 3.4, label, fontsize=13, fontweight="bold", color=TXT, zorder=3)

def box(x, y, w, h, text, fc, ec, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.6",
                                fc=fc, ec=ec, lw=1.8, zorder=4))
    ax.text(x + w / 2, y + h / 2, text, fontsize=fs, color=TXT,
            ha="center", va="center", zorder=5, linespacing=1.45)

def arrow(p1, p2, label=None, dashed=False, both=False, rad=0.0, fs=9,
          lx=0, ly=0, color="#4A6741"):
    style = "<|-|>" if both else "-|>"
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=16,
                                 linestyle=(0, (5, 4)) if dashed else "solid",
                                 color=color, lw=1.7, zorder=3,
                                 connectionstyle=f"arc3,rad={rad}"))
    if label:
        mx, my = (p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly
        ax.text(mx, my, label, fontsize=fs, color=color, ha="center", va="center",
                zorder=6, style="italic",
                bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.2))

def channel(pts, label=None, lpos=None, color="#A08432", dashed=True, both=False, fs=9):
    """Ломаная линия со стрелкой на конце (и в начале, если both)."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, lw=1.7, zorder=3,
            linestyle=(0, (5, 4)) if dashed else "solid", solid_capstyle="round")
    ax.annotate("", xy=pts[-1], xytext=pts[-2], zorder=3,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=16, color=color, lw=1.7))
    if both:
        ax.annotate("", xy=pts[0], xytext=pts[1], zorder=3,
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=16, color=color, lw=1.7))
    if label and lpos:
        ax.text(lpos[0], lpos[1], label, fontsize=fs, color=color, ha="center", va="center",
                zorder=6, style="italic",
                bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.2))

# ---- Группы ----
group(2, 10, 38, 74, "КЛИЕНТЫ", "#E8F0E8", "#5B7A5E")
group(46, 10, 52, 74, "НАШ СЕРВЕР — Selectel VDS (~200 ₽/мес)", "#EFF4E9", "#4A6741")
group(102, 10, 38, 74, "ВНЕШНИЕ СЕРВИСЫ", "#F6F0E3", "#A08432")

# ---- Клиенты ----
box(5, 55, 32, 24, "Приложение\nFlutter, Android\n(устанавливается\nиз RuStore)", "#FFFFFF", "#5B7A5E")
box(5, 22, 32, 22, "Браузер\nFlutter Web\n(арендатор с iPhone)", "#FFFFFF", "#5B7A5E")

# ---- Сервер ----
box(50, 58, 20, 20, "Caddy\nHTTPS + статика\nporog-app.ru", "#FFFFFF", "#4A6741", fs=9.5)
box(74, 52, 21, 26, "PocketBase\nAPI + БД + файлы\n+ realtime\napi.porog-app.ru", "#DDE8D5", "#4A6741", fs=9.5)
box(50, 22, 20, 20, "cron\nнапоминания,\nбэкапы", "#FFFFFF", "#4A6741", fs=9.5)

# ---- Внешние ----
box(106, 62, 32, 16, "RuStore\nPush API · Pay API", "#FFFFFF", "#A08432")
box(106, 36, 32, 16, "СМС-провайдер\n(smsaero и т.п.)", "#FFFFFF", "#A08432")
box(106, 14, 32, 14, "S3 Selectel\nбэкапы (позже)", "#FFFFFF", "#A08432")

# ---- Потоки клиент ↔ сервер ----
arrow((37.5, 68), (50, 68), "HTTPS: вход, синхронизация,\nоплаты, показания, фото",
      both=True, rad=-0.12, ly=8, lx=-1)
arrow((37.5, 36), (50.5, 57), "HTTPS", both=True, rad=-0.15, lx=-3, ly=2.5)

# ---- Внутри сервера ----
arrow((70.5, 66), (73.5, 65.5), "")
arrow((70.5, 34), (74.5, 51), "")

# ---- Сервер ↔ внешние ----
arrow((95.5, 59), (105.5, 48), "отправить код\n(HTTP API)", lx=3, ly=-1)
arrow((95.5, 70), (105.5, 70), "Push API · Pay API", both=True, lx=4, ly=4.5)
arrow((70.5, 29), (105.5, 22), "ежедневный бэкап", dashed=True, rad=-0.1,
      ly=-3.5, color="#6B7280")

# ---- Каналы к телефону поверх схемы ----
channel([(105.8, 44), (103.5, 44), (103.5, 87), (14, 87), (14, 79.5)],
        "СМС с кодом", lpos=(58, 88.8))
channel([(122, 78.5), (122, 92), (30, 92), (30, 79.5)],
        "push-уведомления · подписка (Pay SDK)", both=True, lpos=(72, 93.6))

ax.text(71, 4, "Архитектура серверной части «Порог» · docs/server-arkhitektura.md",
        fontsize=10, color="#6B7280", ha="center", style="italic")

plt.tight_layout()
plt.savefig("docs/server-arkhitektura.png", dpi=150, bbox_inches="tight", facecolor="white")
print("OK")
