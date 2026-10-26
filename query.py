from pony.orm import db_session, select
import datetime as dt
import random as r
from pony import orm

# nomiDottori = ['Marco', 'Andrea', 'Sara', 'Mara', 'Anna', 'Giacomo']
# cognomDottori = ['Bruni', 'Verdi', 'Gialli', 'Grigi', 'Rossi', 'Bianchi']
# CFdottori = ['BRNMRC78E14F205X', 'VRDNDR67S03H501J', 'GLLSRA75B19F205P', 'GRGMRA70M27D969V', 'RSSNNA67D10G702Y', 'BNCGCM64P10G273A']
# nomiInfermieri = ['Giovanna', 'Luca', 'Luigi', 'Manuela', 'Antonio', 'Maurizio', 'Debora', 'Ilaria']
# cognomiInfermieri = ['Carli', 'Bianchi', 'Rossi', 'Gialli', 'Verdi', 'Neri', 'Neri', 'Grigi']
# CFinfermieri = ['CRLGVN64D22H703Q', 'BNCLCU78T01F205Z', 'RSSLGI70M27D969K', 'GLLMNL67T05E289S', 'VRDNTN64L25H501R', 'NRIMRZ64M14F205T', 'NRIDBR64D22H703C', 'GRGLRA64M18D969N']
# nomiPazienti = ['Maria', 'Carla', 'Giovanni', 'Lucia', 'Michele', 'Giuseppe', 'Michela', 'Franco', 'Lisa', 'Gianluca', 'Cristina', 'Lorenza', 'Elena', 'Fabiola', 'Paolo', 'Angelo']
# cognomiPazienti = ['Rossi', 'Neri', 'Bianchi', 'Verdi', 'Carli', 'Carli', 'Bianchi', 'Bruni', 'Bruni','Verdi', 'Gialli', 'Gialli', 'Rossi', 'Rossi', 'Neri', 'Grigi']
# dateNascita = ['14/05/1978', '03/11/1967', '10/09/1945', '12/01/2011', '25/07/2012', '05/11/2015', '30/03/2008', '01/12/1998', '14/04/2000','22/04/1938', '18/09/2013', '07/06/1995', '19/02/1975', '27/08/1970', '15/08/2007', '22/04/2004']



@db_session()
def check_riempimento(Utente, Data, Sala, Prestazione, Ambulatorio, Visita):
        u = list(Utente.select())
        d = list(Data.select())
        s = list(Sala.select())
        p = list(Prestazione.select())
        a = list(Ambulatorio.select())
        v = list(Visita.select())

        if u != [] and d != [] and s != [] and p != [] and a != [] and v != []:
                return True
        else:
                return False
        


@db_session()
def fill_date(Data):
        i = 0
        d = dt.datetime.today().date()
        while d != dt.date(2026, 12, 31):
                d = dt.datetime.today().date() + dt.timedelta(i)
                Data(
                        data_reale=d
                )
                i += 1


@db_session()
def fill_sale(Sala):
        Sala(nome = 'sala1', tipo ='medicazione')
        Sala(nome='sala2', tipo='prelievi')

@db_session()
def fill_ambulatori(Ambulatorio):
                Ambulatorio(nome = 'ambulatorio1', tipo ='adulti')
                Ambulatorio(nome = 'ambulatorio2', tipo ='adulti')
                Ambulatorio(nome = 'ambulatorio3', tipo ='adulti')
                Ambulatorio(nome = 'ambulatorio4', tipo ='pediatria')


@db_session()
def fill_visite(Visita, Data):

        h = []
        i = 0
        while dt.time(18, 30) not in h:
                h.append(dt.time(8+i, 0))
                h.append(dt.time(8+i, 30))
                i += 1
        
        d = Data.select()
        for dv in d:
               for ora in h:
                        Visita(
                                dataVisita = dv,
                                oraVisita = ora.strftime("%H:%M")
                        )


@db_session()
def fill_prestazioni(Prestazione, Data):

        hp = []
        i = 0
        j = 0

        for i in range(11):
                for j in range(6):
                        if dt.time(18, 30) in hp:
                                break
                        else:
                                hp.append(dt.time(8+i, j*10))
   

        d = Data.select()
        for dv in d:
                for ora in hp:
                        Prestazione(
                                dataPrestazione = dv,
                                oraPrestazione = ora.strftime("%H:%M")
                        )


@db_session()
def fill_segreteria(Utente):
        Utente(username='admin', password='pass0')


@db_session()
def check_credentials(username, password, Utente):
    try:
        user = Utente[username, password]
        return True
    except orm.ObjectNotFound:
            pass

    return False



@db_session()
def check_user(username, password, Medico, Infermiere, Paziente, Utente):
        if username=='admin' and password=='pass0':
                return "SEGRETERIA" 
        elif list(select(m for m in Medico if m.credenziale==Utente.get(username=username, password=password))) != []:
                return "MEDICO"
        elif list(select(i for i in Infermiere if i.credenziale==Utente.get(username=username, password=password))) != []:
                return "INFERMIERE"
        elif list(select(p for p in Paziente if p.credenziale==Utente.get(username=username, password=password))) != []:
                return "PAZIENTE"



@db_session()
def checkMail(resp, Paziente):
        resp = resp.split()
        nomeR = resp[0]
        cognomeR = resp[1]
        mail = list(select(p.email for p in Paziente if p.nome==nomeR and p.cognome==cognomeR))
        return mail[0]

@db_session()
def insert_paz(n, c, d, l, em, resp, m, Medico, Paziente, Utente):
        lut = len(list(Utente.select()))
        lenPaz = len(list(Paziente.select()))
        m = m.split()
        nomeM = m[0]
        cognomeM = m[1]
        
        mailPazienti = list(select(p.email for p in Paziente))

        if resp == None:
                if em in mailPazienti:
                        return ["Attenzione! ", "L'email inserita non può essere uguale a quelle già presenti", em+" è già stata inserita"]
                if list(select(p.cssn for p in Paziente if p.nome==n and p.cognome==c and p.dataN==dt.datetime.strptime(d, '%Y-%m-%d').date() and p.luogoN==l and p.email==em)) != []:
                        return  ["Attenzione! ", "Il paziente "+n.upper()+" "+c.upper()+" è già presente!", "Il suo CSSN è: "+list(select(p.cssn for p in Paziente if p.nome==n and p.cognome==c and p.dataN==dt.datetime.strptime(d, '%Y-%m-%d').date() and p.luogoN==l and p.email==em))[0]]
                psw = list(select(u.password for u in Utente))
                psw.sort()
                cssn = list(select(p.cssn for p in Paziente))
                cssn.sort()
                #for i in lut:
                for i in range(len(psw)):
                        if psw[i][4:] != str(i):
                                Utente(
                                        username=n.lower()+"."+c.lower(),
                                        password='pass'+str(i)
                                )
                                for j in range(len(cssn)):
                                        if cssn[j][3:] != str(j):
                                                                # Utente(
                                                                #         username=n.lower()+"."+c.lower(),
                                                                #         password='pass'+str(i)
                                                                #         )
                                                Paziente(
                                                        cssn = 'paz'+str(i),
                                                        nome = n,
                                                        cognome = c,
                                                        dataN = d,
                                                        luogoN = l,
                                                        email = em,
                                                        id_medico = Medico.get(nome=nomeM, cognome=cognomeM),
                                                        credenziale = list(Utente.select())[lut]
                                                )       
                                                return ["Inserimento del paziente "+n.upper()+" "+c.upper()+" avvenuto correttamente!", "USERNAME: "+n.lower()+"."+c.lower()+".", "EMAIL: "+em]
                                
                                Paziente(
                                                cssn = 'paz'+str(lenPaz + 1),
                                                nome = n,
                                                cognome = c,
                                                dataN = d,
                                                luogoN = l,
                                                email = em,
                                                id_medico = Medico.get(nome=nomeM, cognome=cognomeM),
                                                credenziale = list(Utente.select())[lut]
                                        ) 

                               
                # else:
                Utente(
                        username=n.lower()+"."+c.lower(),
                        password='pass'+str(lut)
                )

                for k in range(len(cssn)):
                        if cssn[k][3:] != str(k):
                                Paziente(
                                        cssn = 'paz'+str(k),
                                        nome = n,
                                        cognome = c,
                                        dataN = d,
                                        luogoN = l,
                                        email = em,
                                        id_medico = Medico.get(nome=nomeM, cognome=cognomeM),
                                        credenziale = list(Utente.select())[lut]

                                )
                                return ["Inserimento del paziente "+n.upper()+" "+c.upper()+" avvenuto correttamente!", "USERNAME: "+n.lower()+"."+c.lower(), "EMAIL: "+em]
                
                Paziente(
                                cssn = 'paz'+str(lenPaz + 1),
                                nome = n,
                                cognome = c,
                                dataN = d,
                                luogoN = l,
                                email = em,
                                id_medico = Medico.get(nome=nomeM, cognome=cognomeM),
                                credenziale = list(Utente.select())[lut]

                                )

        else:
                if list(select(p.cssn for p in Paziente if p.nome==n and p.cognome==c and p.dataN==dt.datetime.strptime(d, '%Y-%m-%d').date() and p.luogoN==l)) != []:
                        return  ["Attenzione! ", "Il paziente "+n.upper()+" "+c.upper()+" è già presente!", "Il suo CSSN è: "+list(select(p.cssn for p in Paziente if p.nome==n and p.cognome==c and p.dataN==dt.datetime.strptime(d, '%Y-%m-%d').date() and p.luogoN==l))[0]]
                resp = resp.split()
                nomeResp = resp[0]
                cognomeResp = resp[1]

                Paziente(
                        cssn = 'paz'+str(lenPaz + 1),
                        nome = n,
                        cognome = c,
                        dataN = d,
                        luogoN = l,
                        emailResponsabile = list(select(p.email for p in Paziente if p.nome==nomeResp and p.cognome==cognomeResp))[0],
                        id_responsabile = Paziente.get(nome=nomeResp, cognome=cognomeResp),
                        id_medico = Medico.get(nome=nomeM, cognome=cognomeM)
                )
                return ["Inserimento del paziente "+n.upper()+" "+c.upper()+" avvenuto correttamente!", "Il paziente è minorenne.", "Il suo responsabile è: "+nomeResp.upper()+" "+cognomeResp.upper()]


@db_session()
def tipo_visita(user, psw, Utente, Paziente, minore):
        if minore == None:
                dataPaz = list(select(p.dataN for p in Paziente if p.credenziale==Utente.get(username=user, password=psw)))[0]
                if dataPaz < dt.datetime.strptime('01/01/2010', '%d/%m/%Y').date() and dataPaz > dt.datetime.strptime('31/12/2006', '%d/%m/%Y').date():
                        return "Pediatrica"
                else:
                        return "Adulti"
        else:
                return "Pediatrica"



@db_session()
def checkRes(user, psw, Paziente, Utente):
        cred = Utente.get(username=user, password=psw)
        ut = Paziente.get(credenziale=cred)
        if list(select(p for p in Paziente if p.id_responsabile==ut)) != []:
                return True
        else:
                return False





@db_session()
def seleziona_medico(Medico):
        lista_medici = []
        lista = list(select((m.nome, m.cognome) for m in Medico))
        for l in lista:
                lista_medici.append(l[0]+" "+l[1])
        if lista_medici == None:
                return []
        else:
                return lista_medici



@db_session()
def seleziona_sostituti(med, Medico):
        if med != None:
                lista_medici = []
                med = med.split()
                sostituito = list(select(m for m in Medico if m.nome == med[0] and m.cognome == med[1]))
                lista = list(select((m.nome, m.cognome) for m in Medico if m != sostituito[0]))
                for l in lista:
                        lista_medici.append(l[0]+" "+l[1])
                if lista_medici == None:
                        return []
                else:
                        return lista_medici
        else:
                return []



@db_session()
def seleziona_infermiere(Infermiere):
        lista_inf = []
        lista = list(select((m.nome, m.cognome) for m in Infermiere))
        for l in lista:
                lista_inf.append(l[0]+" "+l[1])
        if lista_inf == None:
                return []
        else:
                return lista_inf



@db_session()
def seleziona_responsabile(Paziente):
        lista_pazienti = []
        lista = list(select((p.nome, p.cognome) for p in Paziente if p.dataN < dt.date(2006, 1, 1)))

        for l in lista:
                lista_pazienti.append(l[0]+" "+l[1])
        if lista_pazienti == None:
                return []
        else:
                return lista_pazienti



@db_session()
def seleziona_paziente(Paziente):
        lista_pazienti = []
        lista = list(select((p.nome, p.cognome) for p in Paziente))

        for l in lista:
                lista_pazienti.append(l[0]+" "+l[1])
        if lista_pazienti == None:
                return []
        else:
                return lista_pazienti




@db_session()
def elimina_med(Medico, Utente, Paziente, Sostituzione, Visita, Data, Controllo, m):
        m = m.split()
        nomem = m[0]
        cognomem = m[1]
        if len(list(Medico.select())) == 1:
                return f"{nomem.upper()} {cognomem.upper()} è l'unico medico rimasto e non può essere eliminato!"
        med = Medico.get(nome=nomem, cognome=cognomem)
        pazmed = list(select(p for p in Paziente if p.id_medico==med))
        l_med = list(select(m for m in Medico if m != med))
        for pz in pazmed:
                pz.id_medico = r.sample(l_med, 1)[0]
        user = select(u for u in Utente if u.username==nomem.lower()+'.'+cognomem.lower())
        if med and user:
                data_oggi = list(select(d for d in Data if d.data_reale >= dt.datetime.today().date()))
                vd = []
                for do in data_oggi:
                        vd.append(list(select(v for v in Visita if v.dataVisita == do))[0])

                for vc in vd:
                        select(c for c in Controllo if c.id_medico == med and c.id_visita == vc).delete()

                mpaz = list(select(c for c in Controllo if c.id_medico == med))

                for mp in mpaz:
                        mp.id_medico = med

               

                date_sel = list(select(sos.dataFine for sos in Sostituzione))
                data_sos = []
                sos_del = []
                for ds in date_sel:
                        data_sos.append(list(select(d.data_reale for d in Data if d == ds and d.data_reale >= dt.datetime.today().date()))[0])
                for dso in data_sos:
                        sos_del.append(list(select(sos for sos in Sostituzioni if (sos.id_sostituto==med or sos.id_sostituire==med) and sos.dataFine == dso))[0])

                
                for ss in sos_del:
                        ss.delete()

                for pz in pazmed:
                        pz.id_medico = r.sample(l_med, 1)[0]
                
                
                med.delete()
                user.delete()
                
               

                return f'Medico {nomem.upper()} {cognomem.upper()} eliminato!'
        else:
                return f'Medico non trovato'


@db_session()
def elimina_inf(Infermiere, Utente, Servizio, Data, Cura, Prestazione, inf):
        inf = inf.split()
        nomei = inf[0]
        cognomei = inf[1]
        if len(list(Infermiere.select())) == 1:
                return f"{nomem.upper()} {cognomem.upper()} è l'unico infermiere rimasto e non può essere eliminato!"
        getInf = Infermiere.get(nome=nomei, cognome=cognomei)
        user = select(u for u in Utente if u.username==nomei.lower()+'.'+cognomei.lower())
        ser = select(se for se in Servizio if se.id_infermiere==getInf)
        if getInf and user and ser:
                data_oggi = list(select(d for d in Data if d.data_reale >= dt.datetime.today().date()))
                pd = []
                for do in data_oggi:
                        pd.append(list(select(p for p in Prestazione if p.dataPrestazione == do))[0])

                for pc in pd:
                        select(c for c in Cura if c.id_infermiere == getInf and c.id_prestazione == pc).delete()

                cuinf = list(select(c for c in Cura if c.id_infermiere == getInf))
                for cui in cuinf:
                        cui.id_infermiere = getInf

                getInf.delete()
                user.delete()
                ser.delete()
                return f'Infermiere/a {nomei.upper()} {cognomei.upper()} eliminato/a!'
        else:
                return f'Infermiere/a non trovato/a'



@db_session()
def elimina_paz(Paziente, Utente, Controllo, Cura, Data, Visita, Prestazione, p):
        p = p.split()
        nomep = p[0]
        cognomep = p[1]
        getPaz = Paziente.get(nome=nomep, cognome=cognomep)

        data_oggi = list(select(d for d in Data if d.data_reale >= dt.datetime.today().date()))
        vd = []
        for do in data_oggi:
                vd.append(list(select(v for v in Visita if v.dataVisita == do))[0])

        for vc in vd:
                select(c for c in Controllo if c.id_paziente == getPaz and c.id_visita == vc).delete()

        cpaz = list(select(c for c in Controllo if c.id_paziente == getPaz))
        for cp in cpaz:
                cp.id_paziente = getPaz

        pd = []
        for do in data_oggi:
                pd.append(list(select(p for p in Prestazione if p.dataPrestazione == do))[0])

        for pc in pd:
                select(c for c in Cura if c.id_paziente == getPaz and c.id_prestazione == pc).delete()

        cupaz = list(select(c for c in Cura if c.id_paziente == getPaz))
        for cup in cupaz:
                cup.id_paziente = getPaz

        user = list(select(u for u in Utente if u.username==nomep.lower()+'.'+cognomep.lower()))

        if user != []:
                up = list(select((u.username, u.password) for u in Utente if u == user[0]))
                username = up[0][0]
                password = up[0][1]
                if getPaz:
                        if checkRes(username, password, Paziente, Utente):
                                getPaz.delete()
                                for u in user:
                                        u.delete()
                                return f'Paziente {nomep.upper()} {cognomep.upper()} eliminato! I suoi minori dovranno essere reinseriti assieme ad un nuovo responsabile!'
                        else:
                                getPaz.delete()
                                for u in user:
                                        u.delete()
                                return f'Paziente {nomep.upper()} {cognomep.upper()} eliminato!'
        else:
                if getPaz:
                        getPaz.delete()
                        return f'Paziente {nomep.upper()} {cognomep.upper()} eliminato!'
                else:
                        return f'Paziente non trovato'




@db_session()
def insert_med(Medico, Utente, cf, n, c, s):
        l = len(list(Utente.select()))
        if list(select(m for m in Medico if m.cod_fis==cf)) != []:
                return ["Attenzione! ", "Il medico "+n.upper()+" "+c.upper()+" è già presente!"]

        if s == None:
                s = " "
        psw = list(select(u.password for u in Utente))
        psw.sort()
        #for i in l:
        #i = 0
        #if 'pass'+str(l) in psw:
        for i in range(len(psw)):
                        
                if psw[i][4:] != str(i):
                                
                        Utente(
                                username=n.lower()+"."+c.lower(),
                                password='pass'+str(i)
                        )

                        Medico(
                                cod_fis = cf,
                                nome = n,
                                cognome = c,
                                specialita = s,
                                credenziale = list(Utente.select())[l]
                        )
                        return "Inserimento del medico "+n.upper()+" "+c.upper()+" avvenuto correttamente!"
                        
        Utente(
                username=n.lower()+"."+c.lower(),
                password='pass'+str(l)
                )
                
        Medico(
                        cod_fis = cf,
                        nome = n,
                        cognome = c,
                        specialita = s,
                        credenziale = list(Utente.select())[l]
                )

        return "Inserimento del medico "+n.upper()+" "+c.upper()+" avvenuto correttamente!"



@db_session()
def insert_inf(Infermiere, Utente, Data, Sala, Servizio, cf, n, c):

        if list(select(inf for inf in Infermiere if inf.cod_fis == cf)) != []:
                return ["Attenzione! ", "L'infermiere "+n.upper()+" "+c.upper()+" è già presente!"]

        dataS = list(Data.select())
        salaS = list(Sala.select())
        # sala1 = salaS[0]
        # sala2 = salaS[1]
        l = len(list(Utente.select()))
        psw = list(select(u.password for u in Utente))
        #print(psw)
        psw.sort()
        #print(psw)
        for i in range(len(psw)):
                print(psw[i])
                if psw[i][4:] != str(i):
                        print('è diverso')
                        Utente(
                                username=n.lower()+"."+c.lower(),
                                password='pass'+str(i)
                        )

                        Infermiere(
                                cod_fis = cf,
                                nome = n,
                                cognome = c,
                                credenziale = list(Utente.select())[l]
                        )
                        for d in dataS:
                                number = r.randint(0, 1)
                                Servizio(
                                        id_infermiere=list(select(inf for inf in Infermiere if inf.cod_fis == cf))[0],
                                        data=d,
                                        cod_sala=salaS[number]
                                )
                        return "Inserimento dell'infermiere/a "+n.upper()+" "+c.upper()+" avvenuto correttamente!"
             
        Utente(
                username=n.lower()+"."+c.lower(),
                password='pass'+str(l)
        )

        Infermiere(
                cod_fis = cf,
                nome = n,
                cognome = c,
                credenziale = list(Utente.select())[l]
        )

        for d in dataS:
                number = r.randint(0, 1)
                Servizio(
                        id_infermiere=list(select(inf for inf in Infermiere if inf.cod_fis == cf))[0],
                        data=d,
                        cod_sala=salaS[number]
                )

        return "Inserimento dell'infermiere/a "+n.upper()+" "+c.upper()+" avvenuto correttamente!"


@db_session()
def seleziona_date_prestazione(Sala, Servizio, Data, tipoP):
        salas = []
        if tipoP == 'Prelievo':
                salas = list(Sala.select())[1]
                
        elif tipoP == 'Medicazione':
                salas = list(Sala.select())[0]
        else:
                return []

  
        dateser = list(select(s.data for s in Servizio if s.cod_sala==salas).order_by(1))
       
        resvis = []

        for dd in dateser:
                dataadd = list(select(d.data_reale for d in Data if d==dd))[0]
             
                if dataadd.strftime("%d/%m/%Y") not in resvis and dataadd > dt.datetime.today().date():
                        resvis.append(dataadd.strftime("%d/%m/%Y"))

     

        return resvis



@db_session()
def seleziona_data(Data):
        dd = []
        dataV = list(select((d.data_reale) for d in Data if d.data_reale >= dt.datetime.today().date()+dt.timedelta(1)))
        for d in dataV:
                dd.append(d.strftime("%d/%m/%Y"))
        if dd == []:
                return []
        else:
                return dd

@db_session()
def orari_visita(Visita):
        oo = []
        oraV = list(select(v.oraVisita for v in Visita)) 
      
        if oraV == []:
                return []
        else:
                return oraV

@db_session()
def orari_prestazione(Prestazione):
        oo = []
        oraP = list(select((p.oraPrestazione) for p in Prestazione))
        
        if oraP == []:
                return []
        else:
                return oraP



@db_session()
def find_medico_conv(user, psw, Paziente, Utente, Medico):
        medpaz = list(select(p.id_medico for p in Paziente if p.credenziale==Utente.get(username=user, password=psw)))[0]
        nc = list(select((m.nome, m.cognome) for m in Medico if m == medpaz))[0]
        if nc == None:
                return []
        else:
                return [(nc[0], nc[1])]



@db_session()
def find_medico(Medico, Paziente, Utente, Sostituzione, Data, user, psw, minorenne, dataVisita):

        if minorenne == None:
                u = Utente.get(username=user, password=psw)
                p = list(select((p.nome, p.cognome) for p in Paziente if p.credenziale == u))
                nome = p[0][0]
                cognome = p[0][1]

        else:
                minorenne = minorenne.split()
                nome = minorenne[0]
                cognome = minorenne[1]

        if dataVisita != None:
                dataVisita = dt.datetime.strptime(dataVisita, '%d/%m/%Y').date()
                data_vis = list(select(d for d in Data if d.data_reale == dataVisita))[0]
                med = list(select(p.id_medico for p in Paziente if p.nome == nome and p.cognome == cognome))
                dinizio = list(select(sos.dataInizio for sos in Sostituzione if sos.id_sostituire==med[0]))
                dfine = list(select(sos.dataFine for sos in Sostituzione if sos.id_sostituire==med[0]))
               
                
                dataI = []
                for di in dinizio:
                        dataI.append(list(select(d.data_reale for d in Data if d==di))[0])
                
                
                
                dataF = []
                for dfi in dfine:
                        dataF.append(list(select(d.data_reale for d in Data if d==dfi))[0])

              
        
                
                sostituto = []
                for i in range(len(dataI)):
                        sostituto = list(select(sos.id_sostituto for sos in Sostituzione if sos.id_sostituire==med[0] and (dataVisita >= dataI[i] and dataVisita <= dataF[i])))
                                
            
                if sostituto != []:
                        nc = list(select((m.nome, m.cognome) for m in Medico if m==sostituto[0]))
                        
                else:
                        nc = list(select((m.nome, m.cognome) for m in Medico if m==med[0]))

                if nc == None:
                        return []
                else:
                        return [(nc[0][0], nc[0][1])]
              
        else:
                return None



@db_session()
def find_paziente(user, psw, Utente, Paziente):
        cred = Utente.get(username=user, password=psw)
        paz = list(select((p.nome, p.cognome) for p in Paziente if p.credenziale==cred))

        nome = paz[0][0]
        cognome = paz[0][1]

        return [nome+" "+cognome]


        

@db_session()
def show_visite_medici(Controllo, Visita, Paziente, Medico, Utente, Data, Ambulatorio, user, psw):

        med_ref = list(select(m for m in Medico if m.credenziale==Utente.get(username=user, password=psw)))[0]
        
        paz_ref = list(select(p for p in Paziente if p.id_medico == med_ref)) #nel for
        #paz_ref = list(select(p for p in Paziente if p.credenziale==Utente.get(username=user, password=psw)))[0]
        elementi_colonne = list(select((c.id_visita, c.id_paziente, c.id_ambulatorio, c.esito, c.regime, c.urgenza, c.tipo, c.note) for c in Controllo if c.note and c.id_medico==med_ref).order_by(1, 2))
        
        
        datav = []
        orav = []
        nomePaz = []
        amb = []
        esitiv = []
        regimev = []
        urgenzav = []
        tipov = []
        notev = []

        for e in elementi_colonne:
                dataorav = list(select((v.dataVisita, v.oraVisita) for v in Visita if v==e[0]))[0]
                datav.append(list(select(d.data_reale for d in Data if d==dataorav[0]))[0].strftime("%d/%m/%Y"))
                orav.append(dataorav[1])
                ncpaz = list(select((p.nome, p.cognome) for p in Paziente if p==e[1]))
                nomePaz.append(ncpaz[0][1]+" "+ncpaz[0][0])
                amb.append(list(select(a.nome for a in Ambulatorio if a == e[2]))[0])
                esitiv.append(e[3])
                regimev.append(e[4])
                urgenzav.append(e[5])
                tipov.append(e[6])
                notev.append(e[7])

   
        return [nomePaz, esitiv, datav, orav, regimev, tipov, amb, urgenzav, notev]



@db_session()
def show_visite(Controllo, Visita, Paziente, Medico, Data, Ambulatorio, paz):
        if paz == None:
                return []

        paz = paz.split()
        nomeP = paz[0]
        cognomeP = paz[1]
        paz_ref = list(select(p for p in Paziente if p.nome==nomeP and p.cognome==cognomeP))[0]
        elementi_colonne = list(select((c.id_visita, c.id_paziente, c.id_medico, c.id_ambulatorio, c.esito, c.regime, c.urgenza, c.tipo, c.note) for c in Controllo if c.note and c.id_paziente==paz_ref).order_by(1, 3))
        
   
        datav = []
        orav = []
        nomeMed = []
        amb = []
        esitiv = []
        regimev = []
        urgenzav = []
        tipov = []
        notev = []

        for e in elementi_colonne:
                dataorav = list(select((v.dataVisita, v.oraVisita) for v in Visita if v==e[0]))[0]
                datav.append(list(select(d.data_reale for d in Data if d==dataorav[0]))[0].strftime("%d/%m/%Y"))
                orav.append(dataorav[1])
                ncmed = list(select((m.nome, m.cognome) for m in Medico if m==e[2]))
                nomeMed.append(ncmed[0][1]+" "+ncmed[0][0])
                amb.append(list(select(a.nome for a in Ambulatorio if a == e[3]))[0])
                esitiv.append(e[4])
                regimev.append(e[5])
                urgenzav.append(e[6])
                tipov.append(e[7])
                notev.append(e[8])

       

        return [nomeMed, esitiv, datav, orav, regimev, tipov, amb, urgenzav, notev]



@db_session()
def show_prestazioni_infermiere(Cura, Prestazione, Paziente, Infermiere, Utente, Data, Sala, user, psw):

        inf_ref = list(select(inf for inf in Infermiere if inf.credenziale==Utente.get(username=user, password=psw)))[0]
        elementi_colonne = list(select((c.id_prestazione, c.id_paziente, c.id_sala, c.esito, c.tipo, c.note) for c in Cura if c.note and c.id_infermiere==inf_ref).order_by(1, 2))
        
        datap = []
        orap = []
        nomePaz = []
        salap = []
        esitip = []
        tipop = []
        notep = []

        for e in elementi_colonne:
                dataorap = list(select((p.dataPrestazione, p.oraPrestazione) for p in Prestazione if p==e[0]))[0]
                datap.append(list(select(d.data_reale for d in Data if d==dataorap[0]))[0].strftime("%d/%m/%Y"))
                orap.append(dataorap[1])
                ncpaz = list(select((p.nome, p.cognome) for p in Paziente if p==e[1]))
                nomePaz.append(ncpaz[0][1]+" "+ncpaz[0][0])
                salap.append(list(select(s.nome for s in Sala if s == e[2]))[0])
                esitip.append(e[3])
                tipop.append(e[4])
                notep.append(e[5])


        return [nomePaz, esitip, datap, orap, tipop, salap, notep]



@db_session()
def show_prestazioni(Cura, Prestazione, Paziente, Infermiere, Data, Sala, paz):

        if paz == None:
                return []

        paz = paz.split()
        nomeP = paz[0]
        cognomeP = paz[1]
        paz_ref = list(select(p for p in Paziente if p.nome==nomeP and p.cognome==cognomeP))[0]

        elementi_colonne = list(select((c.id_prestazione, c.id_infermiere, c.id_sala, c.esito, c.tipo, c.note) for c in Cura if c.note and c.id_paziente==paz_ref).order_by(1, 2))
        
        
        datap = []
        orap = []
        nomeInf = []
        salap = []
        esitip = []
        tipop = []
        notep = []

        for e in elementi_colonne:
                dataorap = list(select((p.dataPrestazione, p.oraPrestazione) for p in Prestazione if p==e[0]))[0]
                datap.append(list(select(d.data_reale for d in Data if d==dataorap[0]))[0].strftime("%d/%m/%Y"))
                orap.append(dataorap[1])
                ncinf = list(select((inf.nome, inf.cognome) for inf in Infermiere if inf==e[1]))
                nomeInf.append(ncinf[0][1]+" "+ncinf[0][0])
                salap.append(list(select(s.nome for s in Sala if s == e[2]))[0])
                esitip.append(e[3])
                tipop.append(e[4])
                notep.append(e[5])


        return [nomeInf, esitip, datap, orap, tipop, salap, notep]


@db_session()
def seleziona_paziente_minore(Utente, Paziente, user, psw):
        u = Utente.get(username=user, password=psw)
        pazRes = list(select(p.cssn for p in Paziente if p.credenziale == u))
        minoreRet = []
        paz = list(select(p for p in Paziente if p.cssn == pazRes[0]))


        minore = list(select((p.nome, p.cognome) for p in Paziente if p.id_responsabile==paz[0]))

        for m in minore:
                minoreRet.append(m[0]+" "+m[1])
        return minoreRet



@db_session()
def show_servizi(Servizio, Data, Infermiere, Sala, dataS):
        if dataS == None:
                return None
        else:
                nomeInf = []
                codSala = []
                dataS = dt.datetime.strptime(dataS, '%d/%m/%Y').date()
                
                data_eff = list(select(d for d in Data if d.data_reale == dataS))
                
                ser = list(select((s.id_infermiere, s.cod_sala) for s in Servizio if s.data == data_eff[0]).order_by(1, 2))
                for s in ser:
                        ncInf = list(select((inf.nome, inf.cognome) for inf in Infermiere if inf==s[0]))
                        nomeInf.append(ncInf[0][1]+" "+ncInf[0][0])
                        codSala.append(list((select(sa.nome for sa in Sala if sa==s[1])))[0])
                return [nomeInf, codSala]



@db_session()
def plan(dataI, dataF, sos, sostituto, Sostituzione, Medico, Data):
        dataI = dt.datetime.strptime(dataI, '%Y-%m-%d').date()
        inizio = list(select(d for d in Data if d.data_reale == dataI))
       
        dataF = dt.datetime.strptime(dataF, '%Y-%m-%d').date()
        fine = list(select(d for d in Data if d.data_reale == dataF))
      
        sos = sos.split()
        sostituire = list(select(m for m in Medico if m.nome==sos[0] and m.cognome==sos[1]))
       
        sostituto = sostituto.split()
        id_sos = list(select(m for m in Medico if m.nome==sostituto[0] and m.cognome==sostituto[1]))
       
        if inizio <= fine:
                Sostituzione(
                        dataInizio = inizio[0],
                        dataFine = fine[0],
                        id_sostituire = sostituire[0],
                        id_sostituto = id_sos[0]
                )
                return ["Inserimento avvenuto correttamente!", "Dal "+dataI.strftime("%d/%m/%Y")+" al "+dataF.strftime("%d/%m/%Y")+" "+sostituto[0].upper()+" "+sostituto[1].upper()+" sostituirà "+sos[0].upper()+" "+sos[1].upper()]



@db_session()
def sel_orario(Data, Medico, Sostituzione, Controllo, Paziente, Utente, Visita, med, dataV): 

        if med == None:
                return []
        
        med = med.split()
        nomeMed = med[0]
        cognomeMed = med[1]
        id_medico = list(select(m for m in Medico if m.nome == nomeMed and m.cognome == cognomeMed))[0]
     
        data_controllo = list(select(d for d in Data if d.data_reale == dt.datetime.strptime(dataV, '%d/%m/%Y').date()))[0]
        controllo_v = list(select(v for v in Visita if v.dataVisita == data_controllo))
        
        id_visita = []
        orari_tot = orari_visita(Visita)
        for cv in controllo_v:
                id_visita = list(select(c.id_visita for c in Controllo if c.id_medico == id_medico and c.id_visita == cv))
                if id_visita != []:
                        orario_add = list(select(v.oraVisita for v in Visita if v in id_visita and v.dataVisita == data_controllo))[0]
                        orari_tot.remove(orario_add)
        if orari_tot == []:
                return orari_visita(Visita)
        else:
                return orari_tot


@db_session()
def sel_date_visita(Data, Controllo, Visita, Utente, Medico, Paziente, user, psw): #METTERE IL CONTROLLO SUL MEDICO
        id_medico = list(select(m for m in Medico if m.credenziale==Utente.get(username=user, password=psw)))[0]
        visite_c = list(select((c.id_visita, c.id_paziente) for c in Controllo if not c.esito and c.id_medico == id_medico).order_by(1, 2))
        dateora_vis = []
        date_vis = []
        datev = []
        for vi in visite_c:
                date_vis = list(select((v.dataVisita, v.oraVisita) for v in Visita if v == vi[0]))[0]
                paziente_vis = list(select((p.nome, p.cognome) for p in Paziente if p == vi[1]))[0]

                
                datev.append([list(select(d.data_reale for d in Data if d == date_vis[0]))[0].strftime("%d/%m/%Y"), date_vis[1], paziente_vis[0], paziente_vis[1]])
           

        for dd in datev:
                dateora_vis.append(str(dd[0])+" "+ str(dd[1])+" "+dd[2]+" "+dd[3])
        
        return [dateora_vis]



@db_session()
def aggiungi_esito(Controllo, Data, Visita, Paziente, Medico, Utente, dataorapaz, esitov, user, psw, urg):
       
        if dataorapaz == None:
                return []

        dataorapaz = dataorapaz.split()
        datav = dt.datetime.strptime(dataorapaz[0], '%d/%m/%Y').date()
        orav = dataorapaz[1]
        nomeP = dataorapaz[2]
        cognomeP = dataorapaz[3]

        data_vis = list(select(d for d in Data if d.data_reale==datav))[0]
        vis = list(select(v for v in Visita if v.dataVisita == data_vis and v.oraVisita == orav))[0]
        paz_vis = list(select(p for p in Paziente if p.nome == nomeP and p.cognome==cognomeP))[0]
        med_vis = list(select(m for m in Medico if m.credenziale==Utente.get(username=user, password=psw)))[0]
        c_esito = list(select(c for c in Controllo if c.id_visita == vis and c.id_paziente == paz_vis and c.id_medico == med_vis))[0]
        if c_esito and 'urgent' in urg:
                c_esito.esito = esitov
                c_esito.urgenza = 'Urgente'
                return "Esito aggiunto. La visita è classificata 'Urgente'"
        else:
                c_esito.esito = esitov
                return "Esito aggiunto! La visita non è urgente."

        return []

@db_session()
def sel_date_seg(Visita, Paziente, Medico, Data, Controllo):
        vpm_seg = list(select((c.id_visita, c.id_paziente, c.id_medico) for c in Controllo if c.esito and not c.note).order_by(1, 2, 3))

        date_seg = []
        for vpm in vpm_seg:
                datav = list(select((v.dataVisita, v.oraVisita) for v in Visita if v == vpm[0]))[0]
                pazv = list(select((p.nome, p.cognome) for p in Paziente if p == vpm[1]))[0]
                medv = list(select((m.nome, m.cognome) for m in Medico if m == vpm[2]))[0]

                date_seg.append([list(select(d.data_reale for d in Data if d == datav[0]))[0].strftime("%d/%m/%Y"), datav[1], pazv[0], pazv[1], medv[0], medv[1]])
        
        dateora_vis = []
        for dd in date_seg:
                dateora_vis.append("Data: "+str(dd[0])+" "+ str(dd[1])+" --- Paziente: "+dd[2]+" "+dd[3]+" --- Medico: "+dd[4]+" "+dd[5])
        
        #print(dateora_vis)
        return [dateora_vis]



@db_session()
def sel_date_seg_pres(Prestazione, Paziente, Infermiere, Data, Cura):
        ppm_seg = list(select((c.id_prestazione, c.id_paziente, c.id_infermiere) for c in Cura if c.esito and not c.note).order_by(1, 2, 3))

        date_seg = []
        for ppm in ppm_seg:
                datap = list(select((p.dataPrestazione, p.oraPrestazione) for p in Prestazione if p == ppm[0]))[0]
                pazp = list(select((p.nome, p.cognome) for p in Paziente if p == ppm[1]))[0]
                infp = list(select((inf.nome, inf.cognome) for inf in Infermiere if inf == ppm[2]))[0]

                date_seg.append([list(select(d.data_reale for d in Data if d == datap[0]))[0].strftime("%d/%m/%Y"), datap[1], pazp[0], pazp[1], infp[0], infp[1]])
        
        dateora_vis = []
        for dd in date_seg:
                dateora_vis.append("Data: "+str(dd[0])+" "+ str(dd[1])+" --- Paziente: "+dd[2]+" "+dd[3]+" --- Infermiere: "+dd[4]+" "+dd[5])
        
        
        return [dateora_vis]


        
@db_session()
def conferma_visita(Controllo, Data, Visita, Paziente, Medico, dataorapazmed, notev):
        if dataorapazmed == None:
                return []

        dataorapazmed = dataorapazmed.split('---')
        paz_tot = dataorapazmed[1].split()
        nomeP = paz_tot[1]
        cognomeP = paz_tot[2]
        ref_paz = Paziente.get(nome=nomeP, cognome=cognomeP)
        data_tot = dataorapazmed[0].split()
        data_vis = list(select(d for d in Data if d.data_reale==dt.datetime.strptime(data_tot[1], '%d/%m/%Y').date()))[0]
        ora_vis = data_tot[2]
        ref_vis = list(select(v for v in Visita if v.dataVisita == data_vis and v.oraVisita == ora_vis))[0]
        med_tot = dataorapazmed[2].split()
        nomeM = med_tot[1]
        cognomeM = med_tot[2]
        ref_med = Medico.get(nome=nomeM, cognome=cognomeM)

        c_note = list(select(c for c in Controllo if c.id_visita == ref_vis and c.id_paziente == ref_paz and c.id_medico == ref_med))[0]

        if c_note:
                if not notev:
                        c_note.note = "Visita effettuata"
                        return "La visita è stata confermata e sarà visibile a medici e pazienti! Non sono state inserite note aggiuntive."
                else:
                        c_note.note = notev
                        return "La visita è stata confermata e sarà visibile a medici e pazienti! Sono state inserite note aggiuntive."



@db_session()
def conferma_prestazione(Cura, Data, Prestazione, Paziente, Infermiere, dataorapazinf, notep):
        if dataorapazinf == None:
                return []

        dataorapazinf = dataorapazinf.split('---')
        paz_tot = dataorapazinf[1].split()
        nomeP = paz_tot[1]
        cognomeP = paz_tot[2]
        ref_paz = Paziente.get(nome=nomeP, cognome=cognomeP)
        data_tot = dataorapazinf[0].split()
        data_pres = list(select(d for d in Data if d.data_reale==dt.datetime.strptime(data_tot[1], '%d/%m/%Y').date()))[0]
        ora_pres = data_tot[2]
        ref_pres = list(select(p for p in Prestazione if p.dataPrestazione == data_pres and p.oraPrestazione == ora_pres))[0]
        inf_tot = dataorapazinf[2].split()
        nomeI = inf_tot[1]
        cognomeI = inf_tot[2]
        ref_inf = Infermiere.get(nome=nomeI, cognome=cognomeI)

        c_note = list(select(c for c in Cura if c.id_prestazione == ref_pres and c.id_paziente == ref_paz and c.id_infermiere == ref_inf))[0]

        if c_note:
                if not notep:
                        c_note.note = "Prestazione effettuata"
                        return "La prestazione è stata confermata e sarà visibile a infermieri e pazienti! Non sono state inserite note aggiuntive."
                else:
                        c_note.note = notep
                        return "La prestazione è stata confermata e sarà visibile a infermieri e pazienti! Sono state inserite note aggiuntive."



@db_session()
def aggiungi_esito_pres(Cura, Data, Prestazione, Paziente, Infermiere, Utente, dataorapaz, esitop, user, psw):
        if dataorapaz == None:
                return []

        dataorapaz = dataorapaz.split()
        datap = dt.datetime.strptime(dataorapaz[0], '%d/%m/%Y').date()
        orap = dataorapaz[1]
        nomeP = dataorapaz[2]
        cognomeP = dataorapaz[3]

        data_pres = list(select(d for d in Data if d.data_reale==datap))[0]
        pres = list(select(p for p in Prestazione if p.dataPrestazione == data_pres and p.oraPrestazione == orap))[0]
        paz_pres = list(select(p for p in Paziente if p.nome == nomeP and p.cognome==cognomeP))[0]
        inf_pres = list(select(inf for inf in Infermiere if inf.credenziale==Utente.get(username=user, password=psw)))[0]
        c_esito = list(select(c for c in Cura if c.id_prestazione == pres and c.id_paziente == paz_pres and c.id_infermiere == inf_pres))[0]
        if c_esito:
                c_esito.esito = esitop
                return "Esito aggiunto"

        return []



@db_session()
def sel_date_prestazione(Data, Cura, Prestazione, Utente, Infermiere, Paziente, user, psw):
        id_infermiere = list(select(inf for inf in Infermiere if inf.credenziale==Utente.get(username=user, password=psw)))[0]
        prestazioni_c = list(select((c.id_prestazione, c.id_paziente) for c in Cura if not c.esito and c.id_infermiere == id_infermiere).order_by(1, 2))
        
        dateora_pres = []
        date_pres = []
        datep = []
        for pr in prestazioni_c:
                date_pres = list(select((p.dataPrestazione, p.oraPrestazione) for p in Prestazione if p == pr[0]))[0]
                paziente_pres = list(select((p.nome, p.cognome) for p in Paziente if p == pr[1]))[0]
           
                datep.append([list(select(d.data_reale for d in Data if d == date_pres[0]))[0].strftime("%d/%m/%Y"), date_pres[1], paziente_pres[0], paziente_pres[1]])
              

        for dd in datep:
                dateora_pres.append(str(dd[0])+" "+ str(dd[1])+" "+dd[2]+" "+dd[3])
        
        return [dateora_pres]



@db_session()
def sel_orari_visita(Controllo, Visita):
        visite_c = list(select(c.id_visita for c in Controllo if not c.esito))
        ore_vis = []
        for vi in visite_c:
                ore_vis.append(list(select(v.oraVisita for v in Visita if v == vi))[0])

        return ore_vis



@db_session() 
def aggiungi_controllo(Controllo, Visita, Ambulatorio, Medico, Paziente, Utente, Data, minore, data_visita, ora_visita, regimeV, tipoV, med, user, psw): #ISOFROMAT ????
        if minore == None:
                ut = list(select(u for u in Utente if u.username==user and u.password==psw))[0]
                paz = list(select(p for p in Paziente if p.credenziale==ut))[0]
        else:
                minore = minore.split()
                paz = list(select(p for p in Paziente if p.nome==minore[0] and p.cognome==minore[1]))[0]
                
        med = med.split()
        nomeMed = med[0]
        cognomeMed = med[1]
        cod_medico = list(select(m for m in Medico if m.nome == nomeMed and m.cognome == cognomeMed))[0]
        dataC = list(select(d for d in Data if d.data_reale == dt.datetime.strptime(data_visita, '%d/%m/%Y').date()))[0]
        ref_visita = list(select(v for v in Visita if v.dataVisita == dataC and v.oraVisita ==ora_visita))[0]
                
        id_amb1 = list(select(a for a in Ambulatorio if a.codice==1))[0]
        id_amb2 = list(select(a for a in Ambulatorio if a.codice==2))[0]
        id_amb3 = list(select(a for a in Ambulatorio if a.codice==3))[0]
        id_amb4 = list(select(a for a in Ambulatorio if a.codice==4))[0]
        id_amb = list(select(a for a in Ambulatorio if a.codice==4))[0]

        id_ambulatori = list(select(a for a in Ambulatorio))
        num = 0

        if tipoV=='Pediatrica':
                id_amb = id_ambulatori[3]
        else:
                if list(Controllo.select()) == []:
                        num = r.sample([0, 1, 2], 1)
                elif list(select(c for c in Controllo if c.id_visita == ref_visita and c.id_ambulatorio == id_amb1)) != []:
                        num = r.sample([1, 2], 1)
                elif list(select(c for c in Controllo if c.id_visita == ref_visita and c.id_ambulatorio == id_amb2)) != []:
                        num = r.sample([0, 2], 1)
                elif list(select(c for c in Controllo if c.id_visita == ref_visita and c.id_ambulatorio == id_amb3))!= []:
                        num = r.sample([0, 1], 1)
                
                print(num)
                id_amb = id_ambulatori[num]

        Controllo(
                id_paziente = paz,
                id_medico = cod_medico,
                id_visita = ref_visita,
                id_ambulatorio = id_amb,
                regime = regimeV,
                tipo = tipoV
        )

        return "Visita aggiunta correttamente!"


@db_session()
def sel_orario_cura(Data, Prestazione, Cura, Sala, dataP, tipoP):
       
        data_cura = list(select(d for d in Data if d.data_reale == dt.datetime.strptime(dataP, '%d/%m/%Y').date()))[0]
       
        if tipoP == 'Prelievo':
                id_sala = list(select(s for s in Sala if s.tipo=='prelievi'))[0]
        else:
                id_sala = list(select(s for s in Sala if s.tipo=='medicazione'))[0]
        
        
        controllo_p = list(select(p for p in Prestazione if p.dataPrestazione == data_cura))
        orari_tot = orari_prestazione(Prestazione)
        
        id_pres = []
        print(id_sala)
        for cp in controllo_p:
                id_pres = list(select(c.id_prestazione for c in Cura if c.id_prestazione == cp and c.id_sala == id_sala))
                
                if id_pres != []:
                        ora_remove = list(select(p.oraPrestazione for p in Prestazione if p in id_pres and p.dataPrestazione == data_cura))[0]
                        orari_tot.remove(ora_remove)
                        
               
        if orari_tot == []:
                return orari_prestazione(Prestazione)
        else:
                return orari_tot




@db_session() #VEDERE
def aggiungi_cura(Cura, Prestazione, Sala, Servizio, Paziente, Data, npaz, data_pres, ora_pres, tipoP): 
        if npaz == None:
                return None
        else:
                npaz = npaz.split()
                paz = list(select(p for p in Paziente if p.nome==npaz[0] and p.cognome==npaz[1]))[0]


        dataC = list(select(d for d in Data if d.data_reale == dt.datetime.strptime(data_pres, '%d/%m/%Y').date()))[0]
        ref_pres = list(select(p for p in Prestazione if p.dataPrestazione == dataC and p.oraPrestazione ==ora_pres))[0]     
        if tipoP == 'Prelievo':
                cod_sala = list(select(s for s in Sala if s.tipo=='prelievi'))[0]
        else:
                cod_sala = list(select(s for s in Sala if s.tipo=='medicazione'))[0]

        infermieri_giornata = list(select(s.id_infermiere for s in Servizio if s.cod_sala==cod_sala and s.data==dataC))

        Cura(
                id_paziente = paz,
                id_prestazione = ref_pres,
                id_infermiere = r.sample(infermieri_giornata, 1)[0],
                id_sala = cod_sala,
                tipo = tipoP
        )

        return "Prestazione aggiunta correttamente!"