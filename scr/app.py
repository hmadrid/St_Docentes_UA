import streamlit as st
import pandas as pd
import os

# Configurar el diseño de la página a "wide"
st.set_page_config(layout="wide")

def main():
    st.title("Estado de Docente por Mail")
    # Leyenda de símbolos
    st.markdown(
        '<div style="margin-bottom:18px;">' 
        '    <span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#1976d2;color:#fff;text-align:center;line-height:18px;font-size:13px;margin-right:6px;vertical-align:middle;">●</span> <span style="margin-right:18px;">Obligatorio</span>'
        '    <span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#ff9800;color:#fff;text-align:center;line-height:18px;font-size:13px;margin-right:6px;vertical-align:middle;">○</span> <span>Optativo</span>'
        '</div>',
        unsafe_allow_html=True
    )
    # Leer el DataFrame limpio desde CSV (ruta correcta)
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "df_ruta_largo.csv"))
    if not os.path.exists(csv_path):
        st.error(f"No se encontró el archivo de datos en: {csv_path}")
        st.stop()
    df_long = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    
    # Crear dos columnas para los campos de entrada
    col1, col2 = st.columns(2)
    with col1:
        correos = df_long['CORREO'].dropna().unique()
        correo_sel = st.selectbox("Selecciona el correo del docente:", sorted(correos))
    with col2:
        rut_inicio = st.text_input("Ingresa los primeros 4 dígitos de tu RUT:", max_chars=4)

    # Validar que se hayan ingresado ambos campos y que el RUT tenga exactamente 4 dígitos
    if correo_sel and rut_inicio:
        if not (rut_inicio.isdigit() and len(rut_inicio) == 4):
            st.error("Por favor, ingresa exactamente 4 dígitos para el RUT.")
            st.stop()
            
        # Verificar que el RUT coincida con el correo
        df_filtrado = df_long[(df_long['CORREO'] == correo_sel) & (df_long['RUT'].astype(str).str.startswith(rut_inicio))]
        
        if df_filtrado.empty:
            st.error("Los datos ingresados no coinciden. Por favor, verifica tu información.")
            st.stop()
            
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