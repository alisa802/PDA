# CO2 līmeņa monitorings

CO2 līmeņa monitoringa sistēma, kas izveidota, izmantojot Python un Flask. Lietotne vizualizē CO2 datus no CSV faila un palīdz analizēt iekštelpu gaisa kvalitāti.

## Instalācija

Izmantojiet pakotņu pārvaldnieku [pip](https://pip.pypa.io/en/stable/), lai instalētu nepieciešamās bibliotēkas.

```bash
pip install flask pandas matplotlib
```
Palaidiet lietotni:
```bash
python app.py
```
Atveriet pārlūkprogrammu adresē:
```bash
http://127.0.0.1:5000/
```
## Lietošana
Programma ļauj:

* Skatīt CO2 datus grafikā
* Skatīt CO2 datus teksta formātā
* Izvēlēties konkrētu dienu detalizētai apskatei

### Kā ievadīt datus
1. Atveriet lietotni pārlūkprogrammā.
2. Izvēlieties režīmu: "Vizuālie Grafiki", lai redzētu diagrammu, vai "Precīzi Skaitļi", lai redzētu skaitliskās vērtības.
3. Izvēlieties dienu no nolaižamās izvēlnes.
4. Programma parādīs CO2 līmeni attiecīgajai dienai un norādīs drošības statusu, izmantojot krāsas:
* 🟢 Normāls: ≤ 800 ppm
* 🟡 Vidējs: 800–1000 ppm
* 🔴 Bīstams: > 1000 ppm


### CSV datu piemērs (`CO2.csv`)


```csv
Day,CO2
1,400
2,850
3,1100
4,950
5,1200
```
## Sagaidāmais rezultāts
* Grafika skats: Līniju vai stabiņu diagramma, kas attēlo CO2 līmeņa izmaiņas laikā. Krāsas norāda drošības līmeņus.
* Datu skats: CO2 skaitliskās vērtības izvēlētajai dienai, kas izceltas atbilstoši drošības kategorijai.

## Projekta struktūra

Galvenie faili un direktorijas:
```bash
PDA/
├── 23_03/
│   ├── templates/
│   │   └── index.html    # HTML veidne grafikiem un datiem
│   ├── CO2.csv           # CSV fails, kas satur CO2 datus
│   └── app.py            # Galvenā Flask lietotne
└── README.md
```
## Analīzes piemērs
Jūs varat testēt programmu ar dažādām CO2 vērtībām:

* Dienas ar CO2 ≤ 800 ppm → Normāli apstākļi
* Dienas ar CO2 starp 800–1000 ppm → Vidējs līmenis, var būt nepieciešama vēdināšana
* Dienas ar CO2 > 1000 ppm → Bīstami, ieteicama tūlītēja vēdināšana

Pievienojot vai modificējot `CO2.csv` failu, varat simulēt apstākļus klasē un novērot, kā reaģē vizualizācija un drošības brīdinājumi.

## Licence
[MIT](https://choosealicense.com/licenses/mit/)
