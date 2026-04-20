# ✍️ SRT to Styled Captions (FFmpeg + Python)
[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![Español](https://img.shields.io/badge/lang-Español-red.svg)](README.es.md)

**Transforma subtítulos SRT aburridos en subtítulos ASS dinámicos y estilizados, y grábalos directamente en tus videos — automáticamente.**

---

## 🎥 Vista Previa
*(Inserta aquí tu imagen de Antes/Después)*

---

## ¿Por qué esta herramienta?
Los subtítulos son esenciales para aumentar la interacción, pero los estilos predeterminados suelen ser difíciles de leer o poco atractivos. Esta herramienta da vida a tus videos convirtiendo archivos `.srt` básicos en pistas `.ass` (Advanced Substation Alpha) con animaciones, colores y fuentes aleatorias, para luego grabarlos directamente en tu video.

---

## ✨ Características

- 🎨 **Estilos Aleatorios** — Fuente, color y tamaño únicos para cada bloque de subtítulo
- 🎬 **Animaciones Dinámicas** — Efectos de entrada y escala integrados mediante etiquetas ASS
- 📐 **Diseño Inteligente** — Ajuste automático de línea y limitación de posición
- ⚡ **Procesamiento por Lotes** — Empareja automáticamente tus archivos `.srt` y `.mp4` para procesarlos en paralelo
- 🐍 **Ligero** — Utiliza la librería estándar de Python y FFmpeg para máxima velocidad

---

## 🚀 Instalación y Uso

### Instalación
```bash
git clone [https://github.com/TuUsuario/nombre-de-tu-repo.git](https://github.com/TuUsuario/nombre-de-tu-repo.git)
cd nombre-de-tu-repo

# Recomendado: usa un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
