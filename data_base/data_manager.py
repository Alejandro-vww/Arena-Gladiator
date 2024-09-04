grpId = {83949:'Copperline', 72127:'Muxus' , 69928:'Cabecilla' , 72401:'Krenko' , 72386:'Cacique' , 67364:'Jefe' , 71470:'Matrona' , 77252:'Bandido' , 71921:'Fisgon' , 66315:'Astuto' , 72389:'Instigador' , 67392:'Minero' , 74640:'Token' , 70386:'Castillo' , 79095:'Montaña' , 66615:'Tesoro'    ,     79096:'Bosque',73476:'Senda de cumbrerriscos',69407:'Terreno aplastador',77365:'Templo de la reina de los dragones',82302:'Foresta karplusana',70755:'Templo del abandono',75857:'Planta de eter central',77261:'Messi',70792:'Terror del monte venus',81664:'Dragon de oro anciano',77302:'Vieja roehuesos',68653:'Niv mizzet',77340:'Tiamat',71485:'Carga temeraria',77520:'Enfurecer',54613:'Fuerza titanica',71520:'Maximizar',69613:'Crecimiento gigante',77317:'Forma salvaje'}
nombre = {'Copperline': 83949, 'Muxus': 72127, 'Cabecilla': 69928, 'Krenko': 72401, 'Cacique': 72386, 'Jefe': 67364, 'Matrona': 71470, 'Bandido': 77252, 'Fisgon': 71921, 'Astuto': 66315, 'Instigador': 72389, 'Minero': 67392, 'Token': 74640, 'Castillo': 70386, 'Montaña': 79095, 'Tesoro': 66615, 'Bosque': 79096, 'Senda de cumbrerriscos': 73476, 'Terreno aplastador': 69407, 'Templo de la reina de los dragones': 77365, 'Foresta karplusana': 82302, 'Templo del abandono': 70755, 'Planta de eter central': 75857, 'Messi': 77261, 'Terror del monte venus': 70792, 'Dragon de oro anciano': 81664, 'Vieja roehuesos': 77302, 'Niv mizzet': 68653, 'Tiamat': 77340, 'Carga temeraria': 71485, 'Enfurecer': 77520, 'Fuerza titanica': 54613, 'Maximizar': 71520, 'Crecimiento gigante': 69613, 'Forma salvaje': 77317}

nombres_ordenados = ['Templo de la reina de los dragones', 'Copperline', 'Senda de cumbrerriscos', 'Foresta karplusana', 'Terreno aplastador', 'Dragon de oro anciano', 'Niv mizzet', 'Enfurecer', 'Messi', 'Carga temeraria', 'Fuerza titanica', 'Terror del monte venus', 'Crecimiento gigante', 'Maximizar', 'Forma salvaje', 'Vieja roehuesos']
ordered_grpId = list(nombre[grp] for grp in nombres_ordenados)


def grp_id_order(card):
    if card in ordered_grpId:
        return ordered_grpId.index(card)
    return 0
