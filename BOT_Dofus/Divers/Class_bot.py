from Divers import fonction_principal as Fct

class BotScript:
    def __init__(self, liste_Action, Dicto_ressource, Dicto_Zaap, Dicto_Caverne, option, pause):
        self.option = option
        self.liste_Action = liste_Action
        self.Dicto_ressource = Dicto_ressource
        self.Dicto_Zaap = Dicto_Zaap
        self.Dicto_Caverne = Dicto_Caverne
        self.pause = pause
        self.action_actuelle = 0
        self.bool_caverne = False
        self.num_carte_caverne = 0
        self.pos_caverne = (0, 0)
        self.script_fini = False
        self.kill_bot = False


    def run_all_action(self):
        while not(self.script_fini):
            self.run_one_action()
            videerreur = Fct.VidePod(self.Dicto_Zaap, self.option, pause=self.pause, baspourcentage=False)
            if videerreur == 1: # VidePod a subis une erreur
                return 1
            if videerreur == 0: #le bot a ete se vider dans le milieu d'une run, saute a la prochaine run
                self.script_fini = True
            if self.kill_bot:
                return 1
        return 0

    def run_one_action(self):
        Action = self.liste_Action[self.action_actuelle]
        if Action[0:5] == 'Go to':
            if (self.bool_caverne):
                pos = Action[6:]
                num_carte = Fct.Go_to_POS_Caverne(int(pos), self.Dicto_Caverne[self.pos_caverne][0],
                                                               self.Dicto_Caverne[self.pos_caverne][1],
                                                               self.Dicto_Caverne[self.pos_caverne][2],
                                                               self.num_carte_caverne, self.option,
                                                               pause=self.pause)
                if num_carte == 1000000:
                    self.bool_caverne = False
                    self.num_carte_caverne = 0
                    for i in range(self.action_actuelle):
                        ind_act = self.action_actuelle - 1 - i
                        act = self.liste_Action[ind_act]
                        if act[0:4] == 'Zaap':
                            self.action_actuelle = ind_act
                            return
                    self.script_fini = True
                    return
                else:
                    if num_carte == 2000000:
                        self.kill_bot = True
                        return
                    else:
                        self.num_carte_caverne = num_carte
            else:
                pos = Action[6:].split(', ')
                NbSauf = int((len(pos) - 3) / 6)
                sauf = {}
                for j in range(NbSauf):
                    sauf[(int(pos[j * 6 + 3]), int(pos[j * 6 + 4]))] = (
                        int(pos[j * 6 + 5]), int(pos[j * 6 + 6]), int(pos[j * 6 + 7]), int(pos[j * 6 + 8]))
                test = Fct.Go_to_POS([int(pos[0]), int(pos[1])], self.option, sauf=sauf, pause=self.pause)
                if test == 1:
                    self.bool_caverne = False
                    self.num_carte_caverne = 0
                    for i in range(self.action_actuelle):
                        ind_act = self.action_actuelle - 1 - i
                        act = self.liste_Action[ind_act]
                        if act[0:4] == 'Zaap':
                            self.action_actuelle = ind_act
                            return
                    self.script_fini = True
                    return
                if test == 2:
                    self.kill_bot = True
                    return
        if Action[0:6] == 'Sortie':
            self.bool_caverne = False
            self.num_carte_caverne = 0
        if Action[0:6] == 'Rentre':
            caverne = tuple(Fct.MAP_POS())
            if caverne in self.Dicto_Caverne:
                self.pos_caverne = caverne
                self.bool_caverne = True
                self.num_carte_caverne = 0
            else:
                for i in range(self.action_actuelle):
                    ind_act = self.action_actuelle - 1 - i
                    act = self.liste_Action[ind_act]
                    if act[0:5] == 'Go to':
                        self.action_actuelle = ind_act
                        return
                self.script_fini = True
                return
        if Action[0:5] == 'Check':
            if self.bool_caverne:
                test = Fct.ressource(self.Dicto_Caverne[self.pos_caverne][3][self.num_carte_caverne], self.option, pause=self.pause)
                if test == 1:
                    self.kill_bot = True
                    return
            else:
                now = tuple(Fct.MAP_POS())
                if now in self.Dicto_ressource:
                    test = Fct.ressource(self.Dicto_ressource[now], self.option, pause=self.pause)
                    if test == 1:
                        self.kill_bot = True
                        return
        if Action[0:4] == 'Zaap':
            test = Fct.zaap(Action[5:], self.Dicto_Zaap, self.option, pause=self.pause)
            if test == 1:
                self.kill_bot = True
                return

        self.action_actuelle = self.action_actuelle + 1
        if self.action_actuelle == len(self.liste_Action):
            self.script_fini = True


class Optionbot:
    def __init__(self):
        self.pm = 4
        self.po = 11
        self.motDePasse = 'darkside94'
        # self.EmplacementViderPod = 'Banque'
        self.EmplacementViderPod = 'Maison'
        self.proprietairemaison = True
        self.codemaison = '8412251'
        self.codecoffre = '8632125'
        self.poisson = 'truite'
        self.nourrir_dragodinde = True
