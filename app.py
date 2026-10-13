import streamlit as st
import pandas as pd

# Configuración de la interfaz
st.set_page_config(page_title="✈️ EuroTrip 2027", layout="wide", initial_sidebar_state="expanded")

# Título Principal
st.title("🧳 Planificador Dinámico: España - Italia 2027")
st.subheader("Selecciona las opciones en la barra lateral para actualizar precios y enlaces por ciudad")
st.markdown("---")

# --- TASA DE CAMBIO (EUR a USD) ---
TASA_CAMBIO = 1.12  # Tasa de conversión: 1 Euro = 1.12 Dólares

# --- CONTEXTO DE LOS ITINERARIOS ---
itinerario_ciudades = {
    "Barcelona": [
        "✨ 23 abr: Llegada a Madrid (10:50 AM), traslado a Atocha, tren a Barcelona y Sant Jordi.",
        "✨ 24 abr: Sagrada Familia y recorrido modernista.",
        "✨ 25 abr: Excursión de día completo a Girona.",
        "✨ 26 abr: Excursión de día completo a Sitges.",
        "✨ 27 abr: Park Güell, Barrio Gótico y El Born.",
        "✨ 28 abr: Vuelo por la mañana a Roma."
    ],
    "Roma": [
        "✨ 28 abr: Llegada y paseo por el centro histórico.",
        "✨ 29 abr: Roma antigua y Coliseo.",
        "✨ 30 abr: Vaticano y sus principales visitas.",
        "✨ 1 may: Recorrido tranquilo por plazas y barrios.",
        "✨ 2 may: Excursión de día completo a Florencia (Tren rápido).",
        "✨ 3 may: Vuelo por la mañana a Madrid."
    ],
    "Madrid": [
        "✨ 3 may: Llegada y paseo por el centro de Madrid.",
        "✨ 4 may: Excursión completa a Toledo.",
        "✨ 5 may: Excursión completa a Segovia.",
        "✨ 6 may: Museo del Prado y tiempo libre.",
        "✨ 7 may: Vuelo de regreso a las 11:30 AM desde Barajas."
    ]
}

# --- MAPEO DE ENLACES DE TU EXCEL CON ETIQUETAS EN DÓLARES ($ USD) ---
links_alojamientos = {
    "Barcelona": {
        "Opción 1 - $ 310 USD pp": "https://www.airbnb.co.cr/rooms/1512152457262736751?adults=8&check_in=2027-04-23&check_out=2027-04-28&search_mode=regular_search&source_impression_id=p3_797a3570-ea4f-4789-89ea-c850c6444174_61386a0a-415e-45a8-b8c7-52a33436dae5_0_1512152457262736751_1&previous_page_section_name=1000&federated_search_id=797a3570-ea4f-4789-89ea-c850c6444174&guests=1",
        "Opción 2 - $ 426 USD pp": "https://www.airbnb.co.cr/rooms/1261692756822483968?adults=8&check_in=2027-04-23&check_out=2027-04-28&search_mode=regular_search&source_impression_id=p3_15b63f89-ed14-42dd-844c-8e9971529ae6_a08c74d6-97e6-45a8-b92b-663d9e929ae4_0_1261692756822483968_14&previous_page_section_name=1000&federated_search_id=15b63f89-ed14-42dd-844c-8e9971529ae6",
        "Opción 3 - $ 387 USD pp": "https://www.airbnb.co.cr/rooms/1623922730425823108?adults=8&check_in=2027-04-23&check_out=2027-04-28&search_mode=regular_search&source_impression_id=p3_aac9ce8b-82bc-4fc1-a228-0681532e9661_532722a1-2f6e-4fa2-ba9b-d4d6004078a2_0_1623922730425823108_3&previous_page_section_name=1000&federated_search_id=aac9ce8b-82bc-4fc1-a228-0681532e9661"
    },
    "Roma": {
        "Opción 1 - $ 373 USD pp (A 20 mins Coliseo)": "https://www.airbnb.co.cr/rooms/1623298203099768546?adults=8&check_in=2027-04-28&check_out=2027-05-03&guests=8&search_mode=regular_search&source_impression_id=p3_70472744-0774-4fe5-8ecc-b74c807abea8_c000b186-0438-4c90-bcd5-6768d39d8ece_0_1623298203099768546_9&previous_page_section_name=1000&federated_search_id=70472744-0774-4fe5-8ecc-b74c807abea8",
        "Opción 2 - $ 339 USD pp": "https://www.airbnb.co.cr/rooms/52329249?adults=8&check_in=2027-04-28&guests=8&search_mode=regular_search&source_impression_id=p3_9ae5d16f-bec0-47a8-af2f-eb554b7b1c00_284714f0-7524-481e-a542-f857b71ad9f8_0_52329249_4&previous_page_section_name=1000&federated_search_id=9ae5d16f-bec0-47a8-af2f-eb554b7b1c00&review_page_entrypoint=show_all&check_out=2027-05-03"
    },
    "Madrid": {
        "Opción 1 - $ 301 USD pp": "https://www.airbnb.co.cr/rooms/16993980?adults=8&check_in=2027-05-03&check_out=2027-05-07&search_mode=regular_search&source_impression_id=p3_ddc2b793-4850-4c8a-83ff-8e5632fb7e86_2c5c7aca-8de2-4dfa-afee-7ac9f5e83da3_0_16993980_1&previous_page_section_name=1000&federated_search_id=ddc2b793-4850-4c8a-83ff-8e5632fb7e86",
        "Opción 2 - $ 256 USD pp": "https://www.airbnb.co.cr/rooms/11990713?adults=8&check_in=2027-05-03&check_out=2027-05-07&search_mode=regular_search&source_impression_id=p3_dcecc70d-f6ad-4099-92f0-45d6cd9fa507_a61243b5-47dd-4ed8-845a-969d743b92e4_0_11990713_1&previous_page_section_name=1000&federated_search_id=dcecc70d-f6ad-4099-92f0-45d6cd9fa507",
        "Opción 3 - $ 353 USD pp (Chamartín) ": "https://www.airbnb.co.cr/rooms/1378934591316351999?adults=8&check_in=2027-05-03&check_out=2027-05-07&search_mode=regular_search&source_impression_id=p3_1791847224_P3B7e6o33BmQ_gzR&previous_page_section_name=1001&federated_search_id=c4d7d3e0-8f53-4492-af94-3c8bcd850e90&review_page_entrypoint=show_all"
    }
}

# --- COSTOS BASE EN EUROS ---
costo_esim_eur = 50.5
costo_seguro_eur = 57.0
costo_uber_eur = 12.0
costo_vaticano_eur = 25.0
costo_prado_eur = 39.0

costo_sitges_eur = 10.0
costo_girona_eur = 34.8
costo_florencia_eur = 60.0
costo_guell_eur = 10.0

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🗳️ Opciones de Alojamiento")
    st.markdown("Configura la combinación para ver los links en tiempo real:")
    
    st.markdown("---")
    st.subheader("🏠 Alojamientos por Ciudad")
    sel_bcn = st.selectbox("Alojamiento BCN:", list(links_alojamientos["Barcelona"].keys()))
    sel_roma = st.selectbox("Alojamiento Roma:", list(links_alojamientos["Roma"].keys()))
    sel_mad = st.selectbox("Alojamiento Madrid:", list(links_alojamientos["Madrid"].keys()))
    
    st.markdown("---")
    st.subheader("🚄 Transportes principales")
    opcion_tren_bcn = st.selectbox("Tren a BCN:", ["Ouigo - $ 33.60 USD", "Iryio - $ 95.20 USD", "Ave Renfe - En espera"])
    opcion_vuelo_roma = st.selectbox("Vuelo a Roma:", ["ITA Airways - $ 80.64 USD - Maleta 18lb", "Ryanair - $ 120.96 USD - Maleta 10kg", "Vueling - $ 142.24 USD - Maleta 10kg"])
    opcion_vuelo_mad = st.selectbox("Vuelo a Madrid:", ["Ryanair - $ 112.00 USD", "Air Europa - $ 119.84 USD", "ITA Airways - En espera"])

    st.markdown("---")
    st.subheader("🗺️ Excursiones y Rutas (Opcionales)")
    incluye_sitges = st.checkbox(f"Ruta a Sitges (+ $ {costo_sitges_eur * TASA_CAMBIO:.2f} USD)", value=False)
    incluye_girona = st.checkbox(f"Ruta a Girona (+ $ {costo_girona_eur * TASA_CAMBIO:.2f} USD)", value=False)
    incluye_florencia = st.checkbox(f"Tren rápido a Florencia (+ $ {costo_florencia_eur * TASA_CAMBIO:.2f} USD)", value=False)
    incluye_guell = st.checkbox(f"Entrada Park Güell (+ $ {costo_guell_eur * TASA_CAMBIO:.2f} USD)", value=False)
    incluye_vaticano = st.checkbox(f"Visita al Vaticano (+ $ {costo_vaticano_eur * TASA_CAMBIO:.2f} USD)", value=False)
    incluye_prado = st.checkbox(f"Museo del Prado (+ $ {costo_prado_eur * TASA_CAMBIO:.2f} USD)", value=False)
    
    st.markdown("---")
    st.subheader("🚄 Trenes desde Madrid")
    opcion_tren_toledo = st.selectbox("Tren a Toledo:", [f"Renfe Avant (Ida y Vuelta) - $ {22.20 * TASA_CAMBIO:.2f} USD", f"Renfe Avant (Solo Ida) - $ {13.90 * TASA_CAMBIO:.2f} USD", "No asistir ($ 0.00 USD)"], index=2)
    opcion_tren_segovia = st.selectbox("Tren a Segovia:", [f"OUIGO - $ {9.00 * TASA_CAMBIO:.2f} USD", f"Renfe Avant - $ {13.90 * TASA_CAMBIO:.2f} USD", f"Renfe AVE / Alvia - $ {20.00 * TASA_CAMBIO:.2f} USD", "No asistir ($ 0.00 USD)"], index=3)

    st.markdown("---")
    st.subheader("🎟️ Modalidades de Entradas (Elegir una sola)")
    sel_sagrada = st.radio("Sagrada Familia:", [f"Entrada simple + audioguía ($ {26 * TASA_CAMBIO:.2f} USD)", f"Visita Guiada ($ {30 * TASA_CAMBIO:.2f} USD)", f"Entrada con acceso a torre ($ {36 * TASA_CAMBIO:.2f} USD)", f"Guiada + acceso a torre ($ {40 * TASA_CAMBIO:.2f} USD)", "No asistir ($ 0.00 USD)"], index=4)
    sel_coliseo = st.radio("Coliseo romano:", [f"24h – Coliseo, Foro Romano y Palatino ($ {18 * TASA_CAMBIO:.2f} USD)", f"24h – Only Arena ($ {18 * TASA_CAMBIO:.2f} USD)", f"Full Experience (2 días consecutivos) ($ {24 * TASA_CAMBIO:.2f} USD)", "No asistir ($ 0.00 USD)"], index=3)

    st.markdown("---")
    st.subheader("🛡️ Logística Adicional")
    incluye_esim = st.checkbox(f"Incluir E-sim (+ $ {costo_esim_eur * TASA_CAMBIO:.2f} USD)", value=False)
    incluye_seguro = st.checkbox(f"Incluir Seguro INS (+ $ {costo_seguro_eur * TASA_CAMBIO:.2f} USD)", value=False)

# --- PROCESAMIENTO MATEMÁTICO DE LOS COMPONENTES ---
precio_tren_usd = 33.60 if "Ouigo" in opcion_tren_bcn else (95.20 if "Iryio" in opcion_tren_bcn else 0.0)
precio_v_roma_usd = 80.64 if "ITA" in opcion_vuelo_roma else (120.96 if "Ryanair" in opcion_vuelo_roma else 142.24)
precio_v_mad_usd = 112.00 if "Ryanair" in opcion_vuelo_mad else (119.84 if "Air Europa" in opcion_vuelo_mad else 0.0)

precio_bcn_usd = 310 if "Opción 1" in sel_bcn else (426 if "Opción 2" in sel_bcn else 387)
precio_roma_usd = 373 if "Opción 1" in sel_roma else 339
precio_mad_usd = 301 if "Opción 1" in sel_mad else (256 if "Opción 2" in sel_mad else 353)

precio_toledo_usd = (22.20 * TASA_CAMBIO) if "Ida y Vuelta" in opcion_tren_toledo else ((13.90 * TASA_CAMBIO) if "Solo Ida" in opcion_tren_toledo else 0.0)
precio_segovia_usd = (9.00 * TASA_CAMBIO) if "OUIGO" in opcion_tren_segovia else ((13.90 * TASA_CAMBIO) if "Renfe Avant" in opcion_tren_segovia else ((20.00 * TASA_CAMBIO) if "AVE / Alvia" in opcion_tren_segovia else 0.0))

sitges_usd = (costo_sitges_eur * TASA_CAMBIO) if incluye_sitges else 0.0
girona_usd = (costo_girona_eur * TASA_CAMBIO) if incluye_girona else 0.0
florencia_usd = (costo_florencia_eur * TASA_CAMBIO) if incluye_florencia else 0.0
guell_usd = (costo_guell_eur * TASA_CAMBIO) if incluye_guell else 0.0
vaticano_usd = (costo_vaticano_eur * TASA_CAMBIO) if incluye_vaticano else 0.0
prado_usd = (costo_prado_eur * TASA_CAMBIO) if incluye_prado else 0.0
esim_usd = (costo_esim_eur * TASA_CAMBIO) if incluye_esim else 0.0
seguro_usd = (costo_seguro_eur * TASA_CAMBIO) if incluye_seguro else 0.0

sagrada_usd = 26.0 * TASA_CAMBIO if "simple" in sel_sagrada else (30.0 * TASA_CAMBIO if "Visita Guiada" in sel_sagrada else (36.0 * TASA_CAMBIO if "acceso a torre" in sel_sagrada and "Guiada" not in sel_sagrada else (40.0 * TASA_CAMBIO if "Guiada + acceso" in sel_sagrada else 0.0)))
coliseo_usd = 18.0 * TASA_CAMBIO if "Foro Romano" in sel_coliseo else (18.0 * TASA_CAMBIO if "Only Arena" in sel_coliseo else (24.0 * TASA_CAMBIO if "Full Experience" in sel_coliseo else 0.0))

total_alojamientos_usd = precio_bcn_usd + precio_roma_usd + precio_mad_usd
total_transporte_usd = (costo_uber_eur * TASA_CAMBIO) + precio_tren_usd + precio_v_roma_usd + precio_v_mad_usd + sitges_usd + girona_usd + florencia_usd + precio_toledo_usd + precio_segovia_usd
total_tours_usd = vaticano_usd + guell_usd + sagrada_usd + coliseo_usd + prado_usd + esim_usd + seguro_usd

gran_total_persona_usd = total_alojamientos_usd + total_transporte_usd + total_tours_usd

from streamlit_gsheets import GSheetsConnection

# --- FUNCIONES DE PERSISTENCIA CON ST-GSHEETS-CONNECTION ---

def cargar_votos():
    try:
        # Creamos la conexión y leemos la hoja de trabajo llamada "votos"
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="votos", ttl=0) # ttl=0 para evitar caché y ver cambios al instante
        df = df.dropna(how="all") # Limpia filas vacías
        return df
    except Exception as e:
        # Estructura de respaldo en caso de que falte configurar la hoja aún
        return pd.DataFrame(columns=["Nombre", "Barcelona", "Roma", "Madrid"])

def guardar_voto(nombre, bcn, roma, mad):
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # 1. Cargamos los votos actuales
    df_actual = cargar_votos()
    
    # 2. Creamos el nuevo registro en formato DataFrame
    nuevo_registro = pd.DataFrame([{
        "Nombre": nombre, 
        "Barcelona": bcn, 
        "Roma": roma, 
        "Madrid": mad
    }])
    
    # 3. Concatenamos el nuevo voto al DataFrame existente
    df_actual = pd.concat([df_actual, nuevo_registro], ignore_index=True)
    
    # 4. Actualizamos la hoja completa en Google Drive usando el método update de la conexión
    conn.update(worksheet="votos", data=df_actual)

# --- CONTENIDO PRINCIPAL (TABS) ---
tab_itinerario, tab_presupuesto, tab_votacion = st.tabs(["🗓️ Ver Itinerarios Diarios", "💰 Presupuesto Dinámico", "🗳️ Votación de Alojamientos"])

with tab_itinerario:
    st.markdown("### 🗓️ Planes Diarios del Viaje con Alojamientos Activos")
    st.write("")
    
    col_izq_itinerario, col_der_alojamientos = st.columns([1.8, 1])
    
    with col_izq_itinerario:
        cit_tabs = st.tabs(["Barcelona", "Roma", "Madrid"])
        
        with cit_tabs[0]:
            st.markdown("#### Ruta en Barcelona")
            for p in itinerario_ciudades["Barcelona"]:
                st.markdown(p)
            if "No asistir" not in sel_sagrada:
                st.markdown("---")
                st.info("💡 **Nota para Sagrada Familia:** Comprar las entradas con **3 o 4 semanas de anticipación**.")

        with cit_tabs[1]:
            st.markdown("#### Ruta en Roma")
            for p in itinerario_ciudades["Roma"]:
                st.markdown(p)
            if incluye_vaticano:
                st.markdown("---")
                st.info("💡 **Nota para el Vaticano:** Comprar con **60 días de anticipación** cuando el tab de Roma está activo.")
            if "No asistir" not in sel_coliseo:
                st.markdown("---")
                st.warning("🏛️ **Notas para el Coliseo:**\n\n• **General:** Las entradas son nominativas. Comprar exactamente con **30 días de anticipación** en la página oficial: [ticketing.colosseo.it](https://ticketing.colosseo.it/es/)\n\n• **24h – Coliseo, Foro Romano y Palatino:** Acceso de 75 minutos al 1.° y 2.° nivel del anfiteatro (terrazas) y 20 minutos en la Arena, más entrada válida por 24 horas al Foro Romano y Monte Palatino.\n\n• **Full Experience:** Válida por dos días consecutivos. Permite una visita de 90 minutos en el Coliseo e incluye acceso a áreas especiales como la Arena, los Subterráneos o el Ático (según la modalidad que elijas y la disponibilidad), además de los sitios arqueológicos completos.")

        with cit_tabs[2]:
            st.markdown("#### Ruta en Madrid")
            for p in itinerario_ciudades["Madrid"]:
                st.markdown(p)
            if "No asistir" not in opcion_tren_toledo:
                st.markdown("---")
                st.info("🏰 **Notas para el Viaje a Toledo:**\n\n• **Origen:** Madrid-Puerta de Atocha - Almudena Grandes\n\n• **Destino:** Toledo (Estación de Tren)\n\n• **Tipo de transporte:** Tren de alta velocidad (Renfe Avant)\n\n• **Tiempo de trayecto:** 33 minutos\n\n• **Características:** Servicio exclusivo de alta velocidad (Media Distancia) para esta ruta. Los trenes son directos y muy frecuentes a lo largo del día.\n\n• **Conexión al centro:** Autobús urbano Líneas 5, 6.1, 6.2 o 12 desde la estación de tren hasta la Plaza de Zocodover (aprox. 10 minutos, 1.40 €) o a pie subiendo por las escaleras mecánicas de Safont.")
            if "No asistir" not in opcion_tren_segovia:
                st.markdown("---")
                st.info(f"⛪ **Notas para el Viaje a Segovia:**\n\n• **Origen:** Madrid-Chamartín-Clara Campoamor\n\n• **Destino:** Segovia-Guiomar\n\n• **Tipo de transporte:** Tren de alta velocidad\n\n• **Opción seleccionada:** {opcion_tren_segovia}\n\n• **Características:** OUIGO (bajo coste, doble piso, pocas frecuencias); Renfe Avant (servicio regular frecuente, preferido); AVE/Alvia (larga distancia, tarifas dinámicas).\n\n• **Conexión al centro:** Autobús urbano Línea 11 desde la estación Segovia-Guiomar hasta el Acueducto (aprox. 15 minutos, 2 €).")
            if incluye_esim:
                st.markdown("---")
                st.info("📱 **Enlace E-sim (Holafly):** Adquiere tu eSIM para el viaje ingresando al [sitio web oficial de Holafly](https://checkout.holafly.com/id/6b4dac80-a92a-4950-8ca6-77675e035b26).")
                    
    with col_der_alojamientos:
        st.markdown("#### 🛌 Alojamientos de esta Ruta")
        st.markdown("Acceso rápido a las opciones seleccionadas actualmente en el menú:")
        st.write("")
        
        with st.container(border=True):
            st.markdown("##### 🇪🇸 Barcelona")
            st.caption(f"Selección: {sel_bcn}")
            st.link_button("🔗 Abrir Airbnb BCN", links_alojamientos["Barcelona"][sel_bcn], use_container_width=True)
            
        st.write("")
        with st.container(border=True):
            st.markdown("##### 🇮🇹 Roma")
            st.caption(f"Selección: {sel_roma}")
            st.link_button("🔗 Abrir Airbnb Roma", links_alojamientos["Roma"][sel_roma], use_container_width=True)
            
        st.write("")
        with st.container(border=True):
            st.markdown("##### 🇪🇸 Madrid")
            st.caption(f"Selección: {sel_mad}")
            st.link_button("🔗 Abrir Airbnb Madrid", links_alojamientos["Madrid"][sel_mad], use_container_width=True)

with tab_presupuesto:
    st.markdown("### 📊 Desglose de Gastos en Vivo por Categoría (En USD)")
    st.metric(label="💰 Cuota Total Estimada por Persona", value=f"$ {gran_total_persona_usd:,.2f} USD")
    st.caption(f"Calculado aplicando una tasa de cambio fija de 1 EUR = {TASA_CAMBIO} USD")
    st.write("")
    
    conceptos_desglosados = {
        "Categoría": ["🏠 Alojamientos", "🚄 Transporte", "🎟️ Tours / Entradas"],
        "Monto ($ USD)": [total_alojamientos_usd, total_transporte_usd, total_tours_usd],
        "Detalle de lo que incluye": [
            "Monto acumulado de las estancias de Barcelona, Roma y Madrid seleccionadas.",
            "Vuelos, trenes de conexión, excursiones (Sitges/Girona/Florencia/Toledo/Segovia) + Uber.",
            "Monumentos activos (Sagrada Familia, Coliseo, Vaticano, Park Güell, Prado), chip E-sim y seguro."
        ]
    }
    df_desglose = pd.DataFrame(conceptos_desglosados)
    col_tabla, col_grafico = st.columns([1.2, 1])
    with col_tabla:
        st.markdown("📋 Resumen de Cuentas")
        st.dataframe(df_desglose, use_container_width=True, hide_index=True)
    with st.expander("🔍 Auditoría detallada del simulador (Costos individuales en USD)", expanded=True):
        st.write(f"• Hospedaje Barcelona: $ {precio_bcn_usd:.2f} USD")
        st.write(f"• Hospedaje Roma: $ {precio_roma_usd:.2f} USD")
        st.write(f"• Hospedaje Madrid: $ {precio_mad_usd:.2f} USD")
        st.write(f"• Interconexión de transporte aéreo/tren activa: $ {(precio_tren_usd + precio_v_roma_usd + precio_v_mad_usd + precio_toledo_usd + precio_segovia_usd):.2f} USD")
        st.write(f"• Excursiones/Tours activos en ruta: $ {(sitges_usd + girona_usd + florencia_usd + guell_usd):.2f} USD")
        st.write(f"• Entradas elegidas (Sagrada F. + Coliseo + Vaticano + Prado): $ {(sagrada_usd + coliseo_usd + vaticano_usd + prado_usd):.2f} USD")
        st.write(f"• Logística (E-sim: $ {esim_usd:.2f} | Seguro: $ {seguro_usd:.2f})")
    with col_grafico:
        st.markdown("📈 Distribución Visual del Gasto")
        st.bar_chart(data=df_desglose, x="Categoría", y="Monto ($ USD)", use_container_width=True)

# --- NUEVA PESTAÑA: VOTACIÓN DE ALOJAMIENTOS ---
with tab_votacion:
    st.markdown("### 🗳️ Votación de Alojamientos Preferidos")
    st.markdown("¡Selecciona tus opciones favoritas para cada ciudad y registra tu voto!")
    st.write("")

    col_form, col_resumen = st.columns([1, 1.2])

    with col_form:
        with st.form("form_votacion", clear_on_submit=True):
            st.markdown("#### 📝 Tu Selección")
            nombre_votante = st.text_input("Tu Nombre / Alias:", placeholder="Ej. Carlos")
            
            voto_bcn = st.selectbox("Barcelona:", list(links_alojamientos["Barcelona"].keys()), key="voto_bcn")
            voto_roma = st.selectbox("Roma:", list(links_alojamientos["Roma"].keys()), key="voto_roma")
            voto_mad = st.selectbox("Madrid:", list(links_alojamientos["Madrid"].keys()), key="voto_mad")
            
            submitted = st.form_submit_button("📩 Enviar Voto", use_container_width=True)

            if submitted:
                if nombre_votante.strip() == "":
                    st.error("Por favor ingresa tu nombre antes de enviar el voto.")
                else:
                    guardar_voto(nombre_votante.strip(), voto_bcn, voto_roma, voto_mad)
                    st.success(f"¡Gracias {nombre_votante}! Tu voto ha sido registrado con éxito.")
                    st.rerun()

    with col_resumen:
        st.markdown("#### 📊 Votos Registrados")
        df_votos = cargar_votos()

        if df_votos.empty:
            st.info("Aún no hay votos registrados. ¡Sé el primero en votar!")
        else:
            st.dataframe(df_votos, use_container_width=True, hide_index=True)

            st.markdown("##### 🏆 Opciones Más Votadas")
            c1, c2, c3 = st.columns(3)
            with c1:
                top_bcn = df_votos["Barcelona"].mode()[0] if not df_votos["Barcelona"].empty else "N/A"
                st.metric("Top Barcelona", top_bcn.split("-")[0].strip())
            with c2:
                top_roma = df_votos["Roma"].mode()[0] if not df_votos["Roma"].empty else "N/A"
                st.metric("Top Roma", top_roma.split("-")[0].strip())
            with c3:
                top_mad = df_votos["Madrid"].mode()[0] if not df_votos["Madrid"].empty else "N/A"
                st.metric("Top Madrid", top_mad.split("-")[0].strip())
