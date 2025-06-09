import streamlit as st
import pandas as pd
import os

# Configurar el diseño de la página a "wide"
st.set_page_config(layout="wide")

def main():
    st.title("Estado de Docente por Mail")
    # Leer el DataFrame limpio desde CSV (ruta correcta)
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "df_ruta_largo.csv"))
    if not os.path.exists(csv_path):
        st.error(f"No se encontró el archivo de datos en: {csv_path}")
        st.stop()
    df_long = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    
    # Crear dos columnas para los campos de entrada
    col1, col2 = st.columns(2)
    with col1:
        correo_sel = st.text_input("Ingresa tu correo institucional:")
    with col2:
        rut_inicio = st.text_input("Ingresa los primeros 4 dígitos de tu RUT:", max_chars=4)

    # Validar y mostrar información del docente si los datos son correctos
    if correo_sel and rut_inicio:
        if rut_inicio.isdigit() and len(rut_inicio) == 4:
            if correo_sel in df_long['CORREO'].values:
                df_filtrado = df_long[(df_long['CORREO'] == correo_sel) & (df_long['RUT'].astype(str).str.startswith(rut_inicio))]
                if not df_filtrado.empty:
                    nombre_docente = df_filtrado['NOMBRE'].iloc[0]
                    cargo_docente = df_filtrado['CARGO'].iloc[0]
                    perfil_horas = df_filtrado['PERFIL_HORAS'].iloc[0]
                    st.markdown(
                        f'''<div style="font-size:13px;color:#444;margin:12px 0;padding:15px;background-color:#f8f9fa;border-radius:8px;border:1px solid #eee;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                            <style>
                                .info-icon {{
                                    display: inline-block;
                                    width: 16px;
                                    height: 16px;
                                    background-color: #1976d2;
                                    color: white;
                                    border-radius: 50%;
                                    text-align: center;
                                    line-height: 16px;
                                    font-size: 12px;
                                    margin-left: 4px;
                                    cursor: help;
                                    position: relative;
                                }}
                                .info-icon:hover::after {{
                                    content: attr(data-tooltip);
                                    position: absolute;
                                    bottom: 100%;
                                    left: 50%;
                                    transform: translateX(-50%);
                                    background-color: rgba(0,0,0,0.8);
                                    color: white;
                                    padding: 8px;
                                    border-radius: 4px;
                                    font-size: 12px;
                                    white-space: nowrap;
                                    z-index: 1000;
                                    margin-bottom: 5px;
                                }}
                            </style>
                            <span style="margin-right:30px;">
                                <b style="color:#1976d2;">Nombre:</b> {nombre_docente}
                                <span class="info-icon" data-tooltip="Nombre completo del docente">i</span>
                            </span>
                            <span style="margin-right:30px;">
                                <b style="color:#1976d2;">Cargo:</b> {cargo_docente}
                                <span class="info-icon" data-tooltip="Cargo actual en la institución">i</span>
                            </span>
                            <span>
                                <b style="color:#1976d2;">Perfil Horas:</b> {perfil_horas}
                                <span class="info-icon" data-tooltip="Cantidad de horas pedagógicas que docentes adjuntos registran en los períodos vigentes: 1-72, 73-216, o Más de 216">i</span>
                            </span>
                        </div>''',
                        unsafe_allow_html=True
                    )
                    
                    with st.expander("Más información sobre Perfil Horas"):
                        st.markdown("""
                        #### Información adicional sobre perfil de horas:
                        
                        * **1-72 horas:** Docentes con dedicación parcial
                        * **73-216 horas:** Docentes con dedicación media
                        * **Más de 216 horas:** Docentes con dedicación completa
                        * **No Aplica:** Para docentes regulares y otros cargos
                        
                        Esta clasificación determina los requerimientos específicos de la Ruta Docente según la dedicación horaria del académico.
                        
                        ##### Requerimientos por perfil:
                        1. **Dedicación parcial (1-72):**
                           - Cursos habilitantes obligatorios
                           - Flexibilidad en plazos
                        
                        2. **Dedicación media (73-216):**
                           - Cursos habilitantes obligatorios
                           - Algunos cursos iniciales recomendados
                           
                        3. **Dedicación completa (Más de 216):**
                           - Todos los cursos habilitantes
                           - Ruta completa recomendada
                        """)

    # Crear tabs
    tab1, tab2 = st.tabs(["Ruta Docente", "Encuesta Evaluación"])
    
    with tab1:
        # Leyenda de símbolos (después de los campos de entrada)
        st.markdown(
            '<div style="margin:18px 0;">' 
            '    <span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#1976d2;color:#fff;text-align:center;line-height:18px;font-size:13px;margin-right:6px;vertical-align:middle;">●</span> <span style="margin-right:18px;">Obligatorio</span>'
            '    <span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#ff9800;color:#fff;text-align:center;line-height:18px;font-size:13px;margin-right:6px;vertical-align:middle;">○</span> <span>Optativo</span>'
            '</div>',
            unsafe_allow_html=True
        )

        if correo_sel and rut_inicio and rut_inicio.isdigit() and len(rut_inicio) == 4:
            df_filtrado = df_long[(df_long['CORREO'] == correo_sel) & (df_long['RUT'].astype(str).str.startswith(rut_inicio))]
            if not df_filtrado.empty:
                df_mail = df_filtrado
            orden_niveles = ['Habilitante', 'Inicial', 'Avanzado', 'Experto']
            cols = st.columns(4)
            for i, nivel in enumerate(orden_niveles):
                # Calcular el % de avance promedio para el nivel y el correo seleccionado
                df_nivel_mail = df_mail[df_mail['NIVEL'] == nivel]
                if not df_nivel_mail.empty and 'RATIO_AVANCE' in df_nivel_mail.columns:
                    ratio = df_nivel_mail['RATIO_AVANCE'].mean()
                    ratio_pct = f"{ratio*100:.0f}%"
                    progress_html = f'<div style="font-size:15px;margin-bottom:4px;"><b>Avance:</b> <span style="color:#1976d2;font-weight:bold;">{ratio_pct}</span></div>'
                else:
                    progress_html = '<div style="font-size:15px;margin-bottom:4px;"><b>Avance:</b> <span style="color:#888;">N/A</span></div>'
                with cols[i]:
                    st.subheader(nivel)
                    st.markdown(progress_html, unsafe_allow_html=True)
                    df_nivel = df_mail[df_mail['NIVEL'] == nivel][['CURSO', 'ESTADO_CURSO', 'TIPO']].copy()
                    if df_nivel.empty:
                        st.write("-")
                    else:
                        html = ""
                        for _, row in df_nivel.iterrows():
                            estado = str(row['ESTADO_CURSO']).strip().lower()
                            tipo = str(row['TIPO']).strip().lower()
                            if estado == 'aprobado':
                                color = '#b6e7a0'  # verde
                                fontcolor = '#222'
                            elif estado == 'pendiente':
                                color = '#ffe599'  # amarillo
                                fontcolor = '#222'
                            else:
                                color = '#f0f0f0'  # gris
                                fontcolor = '#888'
                            # Badge sutil con símbolo para distinguir tipo
                            if tipo == 'obligatorio':
                                badge = '<span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#1976d2;color:#fff;text-align:center;line-height:18px;font-size:13px;margin-right:8px;vertical-align:middle;">●</span>'
                            elif tipo == 'optativo':
                                badge = '<span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#ff9800;color:#fff;text-align:center;line-height:18px;font-size:13px;margin-right:8px;vertical-align:middle;">○</span>'
                            else:
                                badge = '<span style="display:inline-block;width:18px;margin-right:8px;"></span>'
                            html += f'<div style="background-color:{color};color:{fontcolor};padding:8px 12px;margin-bottom:6px;border-radius:8px;font-size:13px;">{badge}{row["CURSO"]}</div>'
                        st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()