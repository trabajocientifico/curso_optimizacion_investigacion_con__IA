# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Soporte didáctico (sitio estático + materiales) del curso **"Optimización de la investigación científica con IA"** (32 h, 11 sesiones, 4 módulos, 2 entregables) dictado por el PhD Oscar Ivan Vargas Pineda. No es un proyecto de software tradicional: los cambios típicos son de contenido y diseño de presentaciones HTML, no de lógica de aplicación.

- Sitio publicado en GitHub Pages: https://trabajocientifico.github.io/curso_optimizacion_investigacion_con__IA/
- Todo el contenido está en **español** y la audiencia son investigadores.
- Hilo conductor del curso: *"La IA propone. El investigador decide."*

## Commands

No hay build, lint ni tests — es un sitio 100% estático servido desde la raíz por GitHub Pages. Para previsualizar localmente:

```
python -m http.server 8000   # luego abrir http://localhost:8000/
```

(o abrir los .html directamente en el navegador; son autocontenidos). Publicar = commit + push a `main`.

## Architecture

- **`index.html`** — portada del sitio: deck interactivo de ~6 slides (navegación por flechas/dots, tema oscuro/claro con `data-theme`). Contiene **dos arreglos JS duplicados con la estructura del curso**: el roadmap de módulos (`mods`) y el índice de sesiones (`modules`, que genera los enlaces a `index/SesionN_Presentacion_Interactiva.html`). Si se agrega/renombra una sesión hay que actualizar **ambos** arreglos además de crear el archivo de la sesión.
- **`index/`** — presentaciones HTML por sesión (`Sesion0..10_Presentacion_Interactiva.html`) más recursos de apoyo (perfil del docente, catálogo de 24 herramientas IA, PRISMA, jerarquía bibliométrica, generador de prompts, etc.). Cada archivo es un deck **autocontenido**: CSS y JS inline, sin dependencias locales; solo Google Fonts por CDN.
- **Carpetas de materiales (binarios, no código):** `paper/` (PPTX de escritura científica), `documentos/` (plantilla de anteproyecto), `promt/` (prompts del curso), `datos/`, `revistas/`, `desarrollo/`, `CURSO-INVESTIGACION-IA-2026-1/` (notebooks de Colab y exportes WOS/Scopus usados en clase).

## Conventions

- **Identidad visual** (mantener en cualquier HTML nuevo o editado): fondo oscuro `#0d1117`, acento naranja `#ff6b3d`, cian `#3dd6c4`, oro `#e8b04b`; tipografías Fraunces (títulos serif), Sora (texto), Space Mono (kickers/código). Colores por módulo: M1 naranja, M2 oro, M3 cian, M4 `#7c8cff`, cierre `#19c2a8`.
- Los HTML nuevos deben seguir siendo autocontenidos (CSS/JS inline), sin frameworks ni assets locales compartidos.
- Mensajes de commit en español y breves (histórico: "ajuste presentacion").
- El repo vive dentro de una carpeta sincronizada con Google Drive: `.gitignore` excluye punteros de Drive (`*.gsheet`, etc.), `desktop.ini` y temporales de Office (`~$*`). No versionar esos archivos.
