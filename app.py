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
        "Opción 2 - $ 256 USD pp": "https://www.airbnb.co.cr/rooms/11990713?adults=8&check_in=2027-05-03&check_out=2027-05-07&search_mode=regular_search&source_impression_id=p3_dcecc70d-f6ad-4099-92f0-45d6cd9fa507_a61243b5-47dd-4ed8-845a-969d743b92e4_0_11990713_1&previous_page_section_name=1000&federated_search_id=dcecc70d-f6ad-4099-92f0-45d6cd9fa507"
    }
}

# --- COSTOS BASE EN EUROS DESDE EL EXCEL ---
costo_esim_eur = 50.5
costo_seguro_eur = 57.0
costo_uber_eur = 12.0
costo_vaticano_eur = 25.0

# Precios individuales de excursiones de tu Excel
costo_sitges_eur = 10.0
costo_girona_eur = 34.8
costo_florencia_eur = 60.0
costo_guell_eur = 10.0

# --- BARRA LATERAL (DROPDOWNS, CHECKBOXES Y RADIOS INTERACTIVOS) ---
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

    st.markdown("---")
    st.subheader("🎟️ Modalidades de Entradas (Elegir una sola)")
    sel_sagrada = st.radio(
        "Sagrada Familia:",
        [
            f"Entrada simple + audioguía ($ {26 * TASA_CAMBIO:.2f} USD)",
            f"Visita Guiada ($ {30 * TASA_CAMBIO:.2f} USD)",
            f"Entrada con acceso a torre ($ {36 * TASA_CAMBIO:.2f} USD)",
            f"Guiada + acceso a torre ($ {40 * TASA_CAMBIO:.2f} USD)",
            "No asistir ($ 0.00 USD)"
        ], index=0
    )
    
    sel_coliseo = st.radio(
        "Coliseo romano:",
        [
            f"24h – Coliseo, Foro Romano y Palatino ($ {18 * TASA_CAMBIO:.2f} USD)",
            f"24h – Only Arena ($ {18 * TASA_CAMBIO:.2f} USD)",
            f"Full Experience (2 días consecutivos) ($ {24 * TASA_CAMBIO:.2f} USD)",
            "No asistir ($ 0.00 USD)"
        ], index=0
    )

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
precio_mad_usd = 301 if "Opción 1" in sel_mad else 256

# Variables condicionales de checkboxes
sitges_usd = (costo_sitges_eur * TASA_CAMBIO) if incluye_sitges else 0.0
girona_usd = (costo_girona_eur * TASA_CAMBIO) if incluye_girona else 0.0
florencia_usd = (costo_florencia_eur * TASA_CAMBIO) if incluye_florencia else 0.0
guell_usd = (costo_guell_eur * TASA_CAMBIO) if incluye_guell else 0.0
esim_usd = (costo_esim_eur * TASA_CAMBIO) if incluye_esim else 0.0
seguro_usd = (costo_seguro_eur * TASA_CAMBIO) if incluye_seguro else 0.0

# Extracción de valores numéricos de monumentos
sagrada_usd = 26.0 * TASA_CAMBIO if "simple" in sel_sagrada else (30.0 * TASA_CAMBIO if "Visita Guiada" in sel_sagrada else (36.0 * TASA_CAMBIO if "acceso a torre" in sel_sagrada and "Guiada" not in sel_sagrada else (40.0 * TASA_CAMBIO if "Guiada + acceso" in sel_sagrada else 0.0)))
coliseo_usd = 18.0 * TASA_CAMBIO if "Foro Romano" in sel_coliseo else (18.0 * TASA_CAMBIO if "Only Arena" in sel_coliseo else (24.0 * TASA_CAMBIO if "Full Experience" in sel_coliseo else 0.0))

# --- AGRUPACIÓN DEL PRESUPUESTO POR CATEGORÍAS EN USD ---
total_alojamientos_usd = precio_bcn_usd + precio_roma_usd + precio_mad_usd
total_transporte_usd = (costo_uber_eur * TASA_CAMBIO) + precio_tren_usd + precio_v_roma_usd + precio_v_mad_usd + sitges_usd + girona_usd + florencia_usd
total_tours_usd = (costo_vaticano_eur * TASA_CAMBIO) + guell_usd + sagrada_usd + coliseo_usd + esim_usd + seguro_usd

gran_total_persona_usd = total_alojamientos_usd + total_transporte_usd + total_tours_usd

# --- CONTENIDO PRINCIPAL ---
tab_itinerario, tab_presupuesto = st.tabs(["🗓️ Ver Itinerarios Diarios", "💰 Presupuesto Dinámico"])

with tab_itinerario:
    st.markdown("### 🗓️ Planes Diarios del Viaje con Alojamientos Activos")
    st.write("")
    
    # Se define la división formal de las dos columnas de la interfaz
    col_izq_itinerario, col_der_alojamientos = st.columns([1.8, 1])
    
    with col_izq_itinerario:
        cit_tabs = st.tabs(["Barcelona", "Roma", "Madrid"])
        for idx, (nom_ciudad, planes) in enumerate(itinerario_ciudades.items()):
            with cit_tabs[idx]:
                st.markdown(f"#### Ruta en {nom_ciudad}")
                for p in planes:
                    st.markdown(p)
                    
    with col_der_alojamientos:
        st.markdown("#### 🛌 Alojamientos de esta Ruta")
        st.markdown("Acceso rápido a las opciones seleccionadas actualmente en el menú:")
        st.write("")
        
        # CORRECCIÓN DE SANGRÍA: Ahora las tarjetas están anidadas de forma correcta en la columna derecha
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
    "Vuelos, trenes de conexión y excursiones activas (Sitges/Girona/Florencia) + Uber.",
    "Monumentos activos (Sagrada Familia, Coliseo, Vaticano, Park Güell), chip E-sim y seguro."
    ]
    }
    df_desglose = pd.DataFrame(conceptos_desglosados)
    col_tabla, col_grafico = st.columns([1.2, 1])
    with col_tabla:
        st.markdown("📋 Resumen de Cuentas")
        st.dataframe(df_desglose, use_container_width=True, hide_index=True)
    with st.expander("🔍 Auditoría detallada del simulador (Costos individuales en USD)"):
        st.write(f"• Hospedaje Barcelona: $ {precio_bcn_usd:.2f} USD")
        st.write(f"• Hospedaje Roma: $ {precio_roma_usd:.2f} USD")
        st.write(f"• Hospedaje Madrid: $ {precio_mad_usd:.2f} USD")
        st.write(f"• Interconexión de transporte aéreo/tren activa: $ {(precio_tren_usd + precio_v_roma_usd + precio_v_mad_usd):.2f} USD")
        st.write(f"• Excursiones/Tours activos en ruta: $ {(sitges_usd + girona_usd + florencia_usd + guell_usd):.2f} USD")
        st.write(f"• Entradas elegidas (Sagrada F. + Coliseo + Vaticano): $ {(sagrada_usd + coliseo_usd + (costo_vaticano_eur * TASA_CAMBIO)):.2f} USD")
        st.write(f"• Logística (E-sim: $ {esim_usd:.2f} | Seguro: $ {seguro_usd:.2f})")
    with col_grafico:
        st.markdown("📈 Distribución Visual del Gasto")
        st.bar_chart(data=df_desglose, x="Categoría", y="Monto ($ USD)", use_container_width=True)