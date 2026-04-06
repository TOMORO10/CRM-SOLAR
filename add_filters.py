import os
import re

with open('fenoge_crm.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add select tags for dept and ciudad in HTML
html = html.replace(
    '            <select id="filter-impl" onchange="applyFilters()">\n                <option value="">Implementador</option>\n                <!-- Populated dynamically -->\n            </select>',
    '''            <select id="filter-impl" onchange="applyFilters()">
                <option value="">Implementador</option>
                <!-- Populated dynamically -->
            </select>

            <select id="filter-dept" onchange="applyFilters()">
                <option value="">Departamento</option>
                <!-- Populated dynamically -->
            </select>

            <select id="filter-ciudad" onchange="applyFilters()">
                <option value="">Ciudad</option>
                <!-- Populated dynamically -->
            </select>'''
)

# 2. Add population logic in populateSelects()
html = html.replace(
    '''        function populateSelects() {
            var eis = {};
            var impls = {};''',
    '''        function populateSelects() {
            var eis = {};
            var impls = {};
            var depts = {};
            var ciudades = {};'''
)

html = html.replace(
    '''            for(var i=0; i<D.length; i++) {
                if(D[i].ei) eis[D[i].ei] = true;
                if(D[i].impl) impls[D[i].impl] = true;
            }''',
    '''            for(var i=0; i<D.length; i++) {
                if(D[i].ei) eis[D[i].ei] = true;
                if(D[i].impl) impls[D[i].impl] = true;
                if(D[i].dept) depts[D[i].dept] = true;
                if(D[i].ciudad) ciudades[D[i].ciudad] = true;
            }'''
)

html = html.replace(
    '''            var selectImpl = document.getElementById("filter-impl");
            Object.keys(impls).sort().forEach(function(k) {
                var opt = document.createElement("option");
                opt.value = k;
                opt.textContent = k;
                selectImpl.appendChild(opt);
            });
        }''',
    '''            var selectImpl = document.getElementById("filter-impl");
            Object.keys(impls).sort().forEach(function(k) {
                var opt = document.createElement("option");
                opt.value = k;
                opt.textContent = k;
                selectImpl.appendChild(opt);
            });

            var selectDept = document.getElementById("filter-dept");
            Object.keys(depts).sort().forEach(function(k) {
                if(k && k.trim() !== "") {
                    var opt = document.createElement("option");
                    opt.value = k;
                    opt.textContent = k;
                    selectDept.appendChild(opt);
                }
            });

            var selectCiudad = document.getElementById("filter-ciudad");
            Object.keys(ciudades).sort().forEach(function(k) {
                if(k && k.trim() !== "") {
                    var opt = document.createElement("option");
                    opt.value = k;
                    opt.textContent = k;
                    selectCiudad.appendChild(opt);
                }
            });
        }'''
)

# 3. Add to clearFilters
html = html.replace(
    '''            document.getElementById("filter-search").value = "";
            document.getElementById("filter-e2").value = "";
            document.getElementById("filter-ei").value = "";
            document.getElementById("filter-impl").value = "";
            document.getElementById("filter-seg").value = "ALL";
            document.getElementById("filter-val").value = "";
            applyFilters();''',
    '''            document.getElementById("filter-search").value = "";
            document.getElementById("filter-e2").value = "";
            document.getElementById("filter-ei").value = "";
            document.getElementById("filter-impl").value = "";
            document.getElementById("filter-dept").value = "";
            document.getElementById("filter-ciudad").value = "";
            document.getElementById("filter-seg").value = "ALL";
            document.getElementById("filter-val").value = "";
            applyFilters();'''
)

# 4. Add to runFiltersAndSort
html = html.replace(
    '''            var fImpl = document.getElementById("filter-impl").value;
            var fSeg = document.getElementById("filter-seg").value;
            var fVal = document.getElementById("filter-val").value;''',
    '''            var fImpl = document.getElementById("filter-impl").value;
            var fSeg = document.getElementById("filter-seg").value;
            var fVal = document.getElementById("filter-val").value;
            var fDept = document.getElementById("filter-dept").value;
            var fCiudad = document.getElementById("filter-ciudad").value;'''
)

html = html.replace(
    '''                var matchesEi = fEi === "" || c.ei === fEi;
                var matchesImpl = fImpl === "" || c.impl === fImpl;
                var matchesSeg = fSeg === "ALL" || c.seg === fSeg;''',
    '''                var matchesEi = fEi === "" || c.ei === fEi;
                var matchesImpl = fImpl === "" || c.impl === fImpl;
                var matchesSeg = fSeg === "ALL" || c.seg === fSeg;
                var matchesDept = fDept === "" || c.dept === fDept;
                var matchesCiudad = fCiudad === "" || c.ciudad === fCiudad;'''
)

html = html.replace(
    '''                if (matchesSearch && matchesE2 && matchesEi && matchesImpl && matchesSeg && matchesVal) {''',
    '''                if (matchesSearch && matchesE2 && matchesEi && matchesImpl && matchesSeg && matchesVal && matchesDept && matchesCiudad) {'''
)

with open('fenoge_crm.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Additions complete.")
