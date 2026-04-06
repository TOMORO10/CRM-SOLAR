import re

with open('fenoge_crm.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the filter-seg options
old_filter_seg = '''            <select id="filter-seg" onchange="applyFilters()">
                <option value="ALL">Todo el Seguimiento</option>
                <option value="">Sin gestión</option>
                <option value="Pendiente contacto">Pendiente contacto</option>
                <option value="Contactado">Contactado</option>
                <option value="En negociación">En negociación</option>
                <option value="Instalación programada">Instalación programada</option>
                <option value="Instalado">Instalado</option>
                <option value="No interesado">No interesado</option>
            </select>'''

new_filter_seg = '''            <select id="filter-seg" onchange="applyFilters()">
                <option value="ALL">Todo el Seguimiento</option>
                <option value="">No contactado</option>
                <option value="Contactado">Contactado</option>
                <option value="En seguimiento">En seguimiento</option>
                <option value="Contratado">Contratado</option>
                <option value="No interesado">No interesado</option>
            </select>'''
html = html.replace(old_filter_seg, new_filter_seg)

# 2. Update getSegOptions function
old_get_seg_options = '''        function getSegOptions(current) {
            var opts = [
                {v: "", t: "(Sin gestión)"},
                {v: "Pendiente contacto", t: "Pendiente contacto"},
                {v: "Contactado", t: "Contactado"},
                {v: "En negociación", t: "En negociación"},
                {v: "Instalación programada", t: "Instalación programada"},
                {v: "Instalado", t: "Instalado"},
                {v: "No interesado", t: "No interesado"}
            ];'''

new_get_seg_options = '''        function getSegOptions(current) {
            var opts = [
                {v: "", t: "No contactado"},
                {v: "Contactado", t: "Contactado"},
                {v: "En seguimiento", t: "En seguimiento"},
                {v: "Contratado", t: "Contratado"},
                {v: "No interesado", t: "No interesado"}
            ];'''
html = html.replace(old_get_seg_options, new_get_seg_options)

# 3. Update stats-bar HTML
old_stats_bar = '''        <!-- BARRA ESTADISTICAS -->
        <div class="stats-bar">
            <div class="stat-item"><span class="stat-name">Registros Mostrados:</span> <span class="stat-num" id="stat-mostrados">0</span></div>
            <div class="stat-item"><span class="stat-name">Suma Potencia Wp:</span> <span class="stat-num" id="stat-potencia">0</span></div>
            <div class="stat-item"><span class="stat-name">Suma Valor COP:</span> <span class="stat-num" id="stat-valor">$0</span></div>
            <div class="stat-item" style="margin-left:auto"><span class="stat-name">Por subsanar:</span> <span class="stat-num" style="color:var(--yellow)" id="stat-subsanar">0</span></div>
        </div>'''

new_stats_bar = '''        <!-- BARRA ESTADISTICAS -->
        <style>
            .kpi-seg { display: flex; flex-direction: column; align-items: flex-start; }
            .kpi-seg small { font-size: 0.8rem; font-weight: normal; color: #666; margin-top: 2px;}
        </style>
        <div class="stats-bar" style="flex-wrap: wrap;">
            <div class="stat-item"><span class="stat-name">Mostrados:</span> <span class="stat-num" id="stat-mostrados">0</span></div>
            <div class="stat-item" style="border-left: 1px solid #ccc; padding-left: 1rem;"><span class="stat-name" style="color:var(--gray)">No Contactado:</span> <span class="stat-num kpi-seg" id="stat-nocont">0</span></div>
            <div class="stat-item"><span class="stat-name" style="color:var(--blue)">Contactado:</span> <span class="stat-num kpi-seg" id="stat-cont">0</span></div>
            <div class="stat-item"><span class="stat-name" style="color:var(--yellow)">En Seguimiento:</span> <span class="stat-num kpi-seg" id="stat-seg-kpi">0</span></div>
            <div class="stat-item"><span class="stat-name" style="color:var(--green)">Contratado:</span> <span class="stat-num kpi-seg" id="stat-contr">0</span></div>
        </div>'''
html = html.replace(old_stats_bar, new_stats_bar)

# 4. Update updateGlobalStats logic
# We need to replace the fMos, fPot, etc. part in updateGlobalStats()
pattern = re.compile(r'// Stats de los filtrados para la BARRA.*?document\.getElementById\("stat-subsanar"\)\.innerText = fSubsanar;', re.DOTALL)
new_logic = '''// Stats de los filtrados para la BARRA
            var fMos = filteredData.length;
            var sNoContCount = 0, sNoContVal = 0;
            var sContCount = 0, sContVal = 0;
            var sSegCount = 0, sSegVal = 0;
            var sContrCount = 0, sContrVal = 0;

            for(var j=0; j<filteredData.length; j++) {
                var c = filteredData[j];
                var v = c.val || 0;
                var st = c.seg || "";

                if(st === "Contactado") { sContCount++; sContVal += v; }
                else if(st === "En seguimiento") { sSegCount++; sSegVal += v; }
                else if(st === "Contratado") { sContrCount++; sContrVal += v; }
                else if(st === "No interesado") { /* opcionalmente ignorado en kpis de suma o categorizado aparte */ }
                else { sNoContCount++; sNoContVal += v; }
            }

            document.getElementById("stat-mostrados").innerText = fMos;
            document.getElementById("stat-nocont").innerHTML = sNoContCount + " <small>(" + formatCurrency(sNoContVal) + ")</small>";
            document.getElementById("stat-cont").innerHTML = sContCount + " <small>(" + formatCurrency(sContVal) + ")</small>";
            document.getElementById("stat-seg-kpi").innerHTML = sSegCount + " <small>(" + formatCurrency(sSegVal) + ")</small>";
            document.getElementById("stat-contr").innerHTML = sContrCount + " <small>(" + formatCurrency(sContrVal) + ")</small>";'''

html = pattern.sub(new_logic, html)

with open('fenoge_crm.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("KPIs updated successfully.")
