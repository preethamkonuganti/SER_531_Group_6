from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON

def search(request):
    return render(request, 'search.html')

def results_view(request):
    if request.method == 'POST':
        arrested = request.POST.getlist('arrested')
        city = request.POST.getlist('city')
        crime_types = request.POST.getlist('crimeType')
        perpetrator_age = request.POST.getlist('perpetratorAge')
        perpetrator_sex = request.POST.getlist('perpetratorSex')
        victim_age = request.POST.getlist('victimAge')
        victim_sex = request.POST.getlist('victimSex')
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        for i in range(len(crime_types)):
            crime_types[i] = crime_types[i].replace(" ","")

        jena_server_url = 'http://34.94.107.22:3030/crimereport'
        sparql = SPARQLWrapper(jena_server_url)

        sparql_query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX Project: <http://www.semanticweb.org/Team6/ontologies/2023/10/531_Project#>

            SELECT ?id ?actualCrimeType ?arrested ?date ?page ?psex ?vage ?vsex ?block ?ward ?district ?city ?latitude ?longitude
            WHERE {
                ?crime rdf:type Project:Crime.
                OPTIONAL {?crime Project:hasCaseID ?id}
                OPTIONAL {?crime Project:isOfType ?crimeType.}
                OPTIONAL {?crime Project:isArrested ?arrested.} 
                OPTIONAL {?crime Project:hasPerpetrator ?perpetrator.}
                OPTIONAL {?perpetrator Project:perpAge ?page.}
                OPTIONAL {?perpetrator Project:perpSex ?psex.}
                OPTIONAL {?crime Project:hasVictim ?victim.}
                OPTIONAL {?victim Project:victimAge ?vage.}
                OPTIONAL {?victim Project:victimSex ?vsex.}
                OPTIONAL {?crime Project:occuredAt ?location.}
                OPTIONAL {?location Project:hasBlockAddress ?block.}
                OPTIONAL {?location Project:inDistrict ?district.}
                OPTIONAL {?location Project:inWard ?ward.}
                OPTIONAL {?location Project:isInCity ?city.}
                OPTIONAL {?crime Project:hasDate ?date.}
                OPTIONAL {?location Project:hasLatitude ?latitude.}
                OPTIONAL {?location Project:hasLongitude ?longitude.}
                BIND(strafter(str(?crimeType), "#") AS ?actualCrimeType)
        """

        victim = []
        if crime_types:
            sparql_query += " FILTER(?crimeType IN (" + ", ".join(f"Project:{ct}" for ct in crime_types) + "))"
        if perpetrator_sex:
            sparql_query += " FILTER(?psex IN (" + ", ".join(f'"{ps}"' for ps in perpetrator_sex) + "))"
        if arrested:
            sparql_query += " FILTER(?arrested IN (" + ", ".join(f'"{a}"' for a in arrested) + "))"
        if city:
            sparql_query += " FILTER(?city IN (" + ", ".join(f'"{c}"' for c in city) + "))"
        if perpetrator_age:
            sparql_query += " FILTER(?page IN (" + ", ".join(f'"{c}"' for c in perpetrator_age) + "))"
        if victim_age:
            for j in victim_age:
                if j == "18":
                    for i in range(18):
                        victim.append(i)
                if j == "18-25":
                    for i in range(18,26):
                        victim.append(i)
                if j == "26-45":
                    for i in range(26,46):
                        victim.append(i)
                if j == "46-65":
                    for i in range(46,66):
                        victim.append(i)
                if j == "65+":
                    for i in range(65,100):
                        victim.append(i)
                if j == "U":
                    victim.append(j)
            sparql_query += " FILTER(?vage IN (" + ", ".join(f'"{c}"' for c in victim) + "))"
        if victim_sex:
            sparql_query += " FILTER(?vsex IN (" + ", ".join(f'"{vs}"' for vs in victim_sex) + "))"
        if start_date and end_date:
            sparql_query += f' FILTER(xsd:date(?date) >= "{start_date}"^^xsd:date && xsd:date(?date) <= "{end_date}"^^xsd:date)'
        elif start_date:
            sparql_query += f' FILTER(xsd:date(?date) >= "{start_date}"^^xsd:date)'
        elif end_date:
            sparql_query += f' FILTER(xsd:date(?date) <= "{end_date}"^^xsd:date)'



        sparql_query += "}"

        with open("file.txt", 'w') as output_file:
            output_file.write(sparql_query)


        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()


        results_list = []
        for result in results["results"]["bindings"]:
            result_dict = {
                'id': result.get('id', {}).get('value', ''),
                'actualCrimeType': result.get('actualCrimeType', {}).get('value', ''),
                'arrested': result.get('arrested', {}).get('value', ''),
                'date': result.get('date', {}).get('value', ''),
                'page': result.get('page', {}).get('value', ''),
                'psex': result.get('psex', {}).get('value', ''),
                'vage': result.get('vage', {}).get('value', ''),
                'vsex': result.get('vsex', {}).get('value', ''),
                'block': result.get('block', {}).get('value', ''),
                'ward': result.get('ward', {}).get('value', ''),
                'district': result.get('district', {}).get('value', ''),
                'city': result.get('city', {}).get('value', ''),
                'latitude': result.get('latitude', {}).get('value', ''),
                'longitude': result.get('longitude', {}).get('value', ''),
            }
            results_list.append(result_dict)

        return render(request, 'results.html', {'results': results_list})


    return render(request, 'search.html')