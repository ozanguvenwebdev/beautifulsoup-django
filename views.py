import requests
from bs4 import BeautifulSoup
def usySiralama(request, age, branch):

    age = age
    branch = branch


    SiralamaCift.objects.all().delete()
    
    url = "http://www.danssporu.info/ulusal_siralama_liste.php?goster=" + str(age) + "_acik_" + str(branch)

    page = requests.get(url)
    table = BeautifulSoup(page.content, "html.parser")

    table = table.find("table", { "bgcolor" : "#502020" })

    rows=list()
    for row in table.findAll("tr"):
        elements_of_row = []
        for column in row.findAll("td"):
            column = unicodedata.normalize("NFKD", column.text) ### anlamsız işaretleri ayıklamak için, bi de en sonda ".text" diyerek stringe çeviriyorum
            elements_of_row.append(column)

        rows.append(elements_of_row)

        SiralamaCift.objects.create(
                sira=elements_of_row[0],
                cift=elements_of_row[1],
                kulup=elements_of_row[2],
                puan=elements_of_row[3])

    
    if age == "y2":
        yas = "Yıldızlar"
    elif age == "g":
        yas = "Gençler"
    else:
        yas = "Yetişkinler"

    if branch == "lt":
        brans_ismi = "Latin"
    else:
        brans_ismi = "Standart"

    
    ciftler = SiralamaCift.objects.all()
    ciftler.first().delete()

    context = {
        'ciftler':ciftler,
        'yas': yas,
        'brans_ismi': brans_ismi,
    }
    
    # print(len(rows))
    if len(rows) == 1:
        return render(request, '404.html', context)

        
    return render(request, 'usy-siralama.html', context)

