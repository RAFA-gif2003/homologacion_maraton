# Control de homologación — Maratón Elche–Alicante

Aplicación de campo para la medición de homologación del circuito, trazado **V06**
(42.507,89 m sobre el eje dibujado, previo a homologación).

Funciona íntegramente en el navegador del móvil. No envía nada a ningún servidor
y, una vez cargada por primera vez, arranca sin cobertura.

## Qué hace

En cada parada del homologador, proyecta la posición GPS sobre el eje del recorrido y da:

- el metro del trazado y el kilómetro oficial equivalente (escala *b*);
- la distancia con signo a los puntos kilométricos **a** (cada 1.000 m reales) y **b**
  (paso de 1.007,41539 m, correspondiente a 42,195 km);
- la **longitud final previsible**, a partir del kilómetro que declare el homologador,
  y si sobran o faltan metros respecto a los 42.195 m;
- un registro de paradas exportable a CSV.

## Uso

Abrir en el móvil, conceder el permiso de ubicación y añadir a la pantalla de inicio.
El día de la medición: *Activar GPS*, escribir el kilómetro declarado antes de leer la
posición, *Promediar 30 s* parado, y *Registrar esta parada*.

En los últimos kilómetros el recorrido pasa dos veces casi por el mismo punto, así que
escribir el kilómetro no es opcional: es lo que desambigua la lectura.

## Archivos

| Archivo | Contenido |
| --- | --- |
| `index.html` | Aplicación completa, con el trazado y los 84 puntos embebidos |
| | Incluye foto rotulada por punto y cota GPS, guardadas en el navegador |
| `sw.js` | Service worker: cachea la app para usarla sin red |
| `manifest.webmanifest` | Instalación como aplicación en la pantalla de inicio |
| `icon-192.png`, `icon-512.png` | Iconos |
