import datetime as dt

def ambulatorio_entity(db, orm):
    class Ambulatorio(db.Entity):
        _table_ = 'ambulatorio'
        codice = orm.PrimaryKey(int, auto=True)
        nome = orm.Required(str, 20)
        tipo = orm.Required(str, 10)
        controllo = orm.Set('Controllo')
        
    return Ambulatorio

def controllo_entity(db, orm, Paziente, Visita, Medico, Ambulatorio):
    class Controllo(db.Entity):
        _table_ = 'controllo'
        id_paziente = orm.Required(Paziente, column='CSSNPaziente', cascade_delete=False)
        id_visita = orm.Required(Visita, columns=["data", "ora"])
        id_medico = orm.Required(Medico, column='CFMedico', cascade_delete=False)
        id_ambulatorio = orm.Required(Ambulatorio, column="codAmbulatorio") 
        esito = orm.Optional(str, 200)
        regime = orm.Required(str, 40)
        urgenza = orm.Optional(str,40)
        tipo = orm.Required(str, 50)
        note = orm.Optional(str, 200)
        orm.PrimaryKey(id_paziente, id_visita, id_medico, id_ambulatorio)
    return Controllo


def cura_entity(db, orm, Paziente, Prestazione, Infermiere, Sala):
    class Cura(db.Entity):
        _table_ = 'cura'
        id_paziente = orm.Required(Paziente, column='CSSNPaziente', cascade_delete=False)
        id_prestazione = orm.Required(Prestazione, columns=["data", "ora"])
        id_infermiere = orm.Required(Infermiere, column='CFInfermiere', cascade_delete=False)
        id_sala = orm.Required(Sala, column="codSala") 
        esito = orm.Optional(str, 200)
        note = orm.Optional(str, 200)
        tipo = orm.Required(str, 40)
        orm.PrimaryKey(id_paziente, id_prestazione, id_infermiere, id_sala)
    return Cura



def data_entity(db, orm):
    class Data(db.Entity):
        _table_ = 'data'
        data_reale = orm.PrimaryKey(dt.date)
        dataIM = orm.Set('Sostituzione', reverse='dataInizio')
        dataFM = orm.Set('Sostituzione', reverse='dataFine')
        dataVisita = orm.Set('Visita')
        dataPrestazione = orm.Set('Prestazione')
        dataServizio = orm.Set('Servizio')
    return Data


def infermiere_entity(db, orm, Utente):
    class Infermiere(db.Entity):
        _table_ = 'infermiere'
        cod_fis = orm.PrimaryKey(str, 16)
        nome = orm.Required(str, 40)
        cognome = orm.Required(str, 40)
        credenziale = orm.Required(Utente, columns=["user", "psw"])
        servizio = orm.Set('Servizio')
        cura = orm.Set('Cura')
        
    return Infermiere


def medico_entity(db, orm, Utente, Data):
    class Medico(db.Entity):
        _table_ = 'medico'
        cod_fis = orm.PrimaryKey(str, 16)
        nome = orm.Required(str, 40)
        cognome = orm.Required(str, 40)
        specialita = orm.Optional(str, 40)
        credenziale = orm.Required(Utente, columns=["user", "psw"])
        med_conv = orm.Set('Paziente')
        controllo = orm.Set('Controllo')
        id_sostituto = orm.Set('Sostituzione', reverse="id_sostituire")
        id_sostituito = orm.Set('Sostituzione', reverse="id_sostituto")
    return Medico



def paziente_entity(db, orm, Medico, Utente):
    class Paziente(db.Entity):
        _table_ = 'paziente'
        cssn = orm.PrimaryKey(str, 5)
        nome = orm.Required(str, 40)
        cognome = orm.Required(str, 40)
        dataN = orm.Required(dt.date)
        luogoN = orm.Required(str, 40)
        email = orm.Optional(str, 30, unique=True)
        emailResponsabile = orm.Optional(str, 30)
        id_responsabile = orm.Optional('Paziente', reverse='minore')
        minore = orm.Set('Paziente', reverse='id_responsabile', cascade_delete=True)
        id_medico = orm.Required(Medico, column="id_medico", cascade_delete=False)
        credenziale = orm.Optional(Utente, columns=["user", "psw"])
        controllo = orm.Set('Controllo')
        cura = orm.Set('Cura')
    return Paziente


def prestazione_entity(db, orm, Data):
    class Prestazione(db.Entity):
        _table_ = 'prestazione'
        dataPrestazione = orm.Required(Data, column="dataPrestazione")
        oraPrestazione = orm.Required(str)
        orm.PrimaryKey(dataPrestazione, oraPrestazione)
        cura = orm.Set('Cura')
    return Prestazione


def sala_entity(db, orm):
    class Sala(db.Entity):
        _table_ = 'sala'
        codice = orm.PrimaryKey(int, auto=True)
        nome = orm.Required(str, 6)
        tipo = orm.Required(str, 15)
        cura = orm.Set('Cura')
        servizio = orm.Set('Servizio')
        
    return Sala


def servizio_entity(db, orm, Infermiere, Data, Sala):
    class Servizio(db.Entity):
        _table_ = 'servizio'
        id_infermiere = orm.Required(Infermiere, column='CFInfermiere', cascade_delete=False)
        data = orm.Required(Data, column="dataServizio")
        cod_sala = orm.Required(Sala, column='id_sala')
        orm.PrimaryKey(id_infermiere, data, cod_sala)
        
        
    return Servizio


def sostituzione_entity(db, orm, Medico, Data):
    class Sostituzione(db.Entity):
        _table_ = 'sostituzione'
        dataInizio = orm.Required(Data, column="dataInizioAssenza")
        dataFine = orm.Required(Data, column="dataFineAssenza")
        id_sostituire = orm.Required(Medico, column='sostituito', cascade_delete=False)
        id_sostituto = orm.Required(Medico, column='sostituto', cascade_delete=False)
        orm.PrimaryKey(dataInizio, dataFine, id_sostituire, id_sostituto)
    return Sostituzione


def utente_entity(db, orm):
    class Utente(db.Entity):
        _table_ = 'utente'
        username = orm.Required(str, 300)
        password = orm.Required(str, 20)
        orm.PrimaryKey(username, password)
        credenzialeM = orm.Set('Medico')
        credenzialeI = orm.Set('Infermiere')
        credenzialeP = orm.Set('Paziente')
    return Utente


def visita_entity(db, orm, Data):
    class Visita(db.Entity):
        _table_ = 'visita'
        dataVisita = orm.Required(Data, column="dataVisita")
        oraVisita = orm.Required(str)
        orm.PrimaryKey(dataVisita, oraVisita)
        controllo = orm.Set('Controllo')
    return Visita