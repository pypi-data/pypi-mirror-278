import numpy as np
import random 
import matplotlib.pyplot as plt
import networkx as nx

class cvrp:
    def __init__(self, nb_individus: int, nb_mutation: float, nb_iteration: int, nb_vehicule=3, cp_vehicule=25, nb_client=5, demande_client=None, matrice_distance = None):
        self.nb_vehicule = nb_vehicule
        self.cp_vehicule = cp_vehicule
        self.nb_client = nb_client
        # Initialisation de demande_client
        if demande_client is None:
            self.demande_client = [random.randint(1, 12) for _ in range(self.nb_client)]
        else:
            self.demande_client = demande_client
        # initialisation de matrice_distance
        if matrice_distance is None :
            self.matrice_distance = np.array([[0 if i == j else random.randint(1, 1000) for i in range(self.nb_client + 1)] for j in range(self.nb_client + 1)])
            self.matrice_distance = self.matrice_distance + self.matrice_distance.T
            np.fill_diagonal(self.matrice_distance, 0)
        else :
            self.matrice_distance = matrice_distance
        self.nb_individus = nb_individus
        self.nb_mutation = nb_mutation
        self.nb_iteration = nb_iteration
    
    def PI(self) :
        population = []
        clients = list(range(1, self.nb_client+1))
        #On crée une copie de la liste mélangée en utilisant clients[:]
        #et on l'ajoute à la liste matrice.
        #Ceci garantit que chaque sous-liste dans la matrice est une copie séparée de la liste clients mélangée.
        for _ in range(self.nb_individus) :
            random.shuffle(clients)
            population.append(clients[:])
        return population
    
    def transform(self, solution) :
        trajet_v = [[] for _ in range(self.nb_vehicule)]  # Une liste de listes pour stocker les trajets de chaque véhicule

        cp = self.cp_vehicule # initialiser la capacitè des vehicules
        vehicule_idx = 0  # Indice du véhicule actuel
        trajet_v[vehicule_idx].append(0) # le premier vehicule commence a partir de depot

        for client in solution :
            if self.demande_client[client - 1] <= cp :  # Vérifiez si la demande du client peut être satisfaite
                cp -= self.demande_client[client - 1]
                trajet_v[vehicule_idx].append(client)

        else :
            # Si la demande du client ne peut pas être satisfaite, passez au véhicule suivant
            trajet_v[vehicule_idx].append(0) # le vehicule retourne au dèpot
            vehicule_idx += 1 # avancer vers le prochaine vehicule
            cp = self.cp_vehicule  # Réinitialisez la capacité du vehicule
            trajet_v[vehicule_idx].append(0) # le prochain vehicule commence a partir de dèpot
            trajet_v[vehicule_idx].append(client)
            cp -= self.demande_client[client-1]

        for chemin in trajet_v :
            if len(chemin) == 0 :
                chemin.extend([0, 0])
            elif chemin[-1] != 0 :
                chemin.append(0)

        return trajet_v
    
    def fitness(self, solution):
        trajets_vehicules = self.transform(solution)
        # Calcul du score de fitness
        score = 0
        for trajet in trajets_vehicules:
            for client in range(len(trajet) -1) :
            # Ajouter la distance entre les clients consécutifs dans x
                score += self.matrice_distance[trajet[client]][trajet[client + 1]] #trajet i cest la ligne de client actuelle et le trajet i+1 cest la colonne de prochain client
        return score
    
    def solution_score(self, solution) :
        dict_solution_score = {}
        score = self.fitness(solution)
        dict_solution_score["solution"] = solution
        dict_solution_score["score_fitness"] = score
        return dict_solution_score
    
    def crossover(self, parent1, parent2):
        # Choix du point de croisement
        point_croisement = int(self.nb_client / 2)

        # Création des solutions filles initialisées avec des valeurs nulles
        enfant1 = [0] * len(parent1)
        enfant2 = [0] * len(parent2)

        # Ajout de la partie avant le point de croisement
        enfant1[:point_croisement] = parent1[:point_croisement]
        enfant2[:point_croisement] = parent2[:point_croisement]

        # Ajout de la partie après le point de croisement, en évitant les répétitions
        enfant1_point_croisement = set(enfant1[:point_croisement])
        enfant2_point_croisement = set(enfant2[:point_croisement])

        for client in parent2:
            if client not in enfant1_point_croisement:
                enfant1[point_croisement] = client
                enfant1_point_croisement.add(client)
                break

        for client in parent1:
            if client not in enfant2_point_croisement:
                enfant2[point_croisement] = client
                enfant2_point_croisement.add(client)
                break

        # Compléter les solutions filles avec les éléments manquants
        for i in range(len(parent1)):
            if enfant1[i] == 0:
                for client in parent2:
                    if client not in enfant1_point_croisement:
                        enfant1[i] = client
                        enfant1_point_croisement.add(client)
                        break

            if enfant2[i] == 0:
                for client in parent1:
                    if client not in enfant2_point_croisement:
                        enfant2[i] = client
                        enfant2_point_croisement.add(client)
                        break

        return enfant1, enfant2
    
    def creation_nouvelle_generation(self, population) :
         nouvelle_generation = []
         for _ in range(self.nb_individus) :
             parent1, parent2 = random.sample(population, k= 2) # selection de deux parents aleatoirement
             enfant1, enfant2 = self.crossover(parent1, parent2) # appelle a la fonction croisement pour generer deux solutions enfants a partir des deux parents
             nouvelle_generation.extend([parent1, parent2, enfant1[:], enfant2[:]]) # ajouter a la nouvelle generation les deux enfants avec leurs parents
         return nouvelle_generation
    
    def selectionGen(self , generation):
         meilleurs_solutions = sorted(generation, key=lambda x: x['score_fitness'], reverse= True)
         meilleurs_solutions = meilleurs_solutions[:self.nb_individus]
         return meilleurs_solutions
    
    def mutation(self, generation):
        taux_mutation = int((self.nb_mutation * self.nb_individus) / 100)
        # choisir k solutions aleatoire
        Solution_aleatoires = random.sample(generation, k= taux_mutation)
        # choisir un client aleatoire
        client = random.choice(range(self.nb_client-1))

        # faire la permutation entre les deux client de la solution
        for solution_aleatoire in Solution_aleatoires :
            x = solution_aleatoire["solution"][client]
            solution_aleatoire["solution"][client] = solution_aleatoire["solution"][client + 1]
            solution_aleatoire["solution"][client + 1] = x

        # dans cette partie on va calculer le score fitness de la solution apres le changement
        for solution_aleatoire in Solution_aleatoires :
            score = self.fitness(solution_aleatoire['solution'])
            solution_aleatoire["score_fitness"] = score
    
    def best_solution(self) :
        Solutions_optimales = []
        population = self.PI()
        # creation de graphe (solution optimale - nombre de generation )
        solutions_optimales = [] # liste qui contient les solutions optimales des differentes generations

        for _ in range(self.nb_iteration) :
            if _ == 0 : # dans la premeire iteration on prend la population initiale pour develloper une la nouvelle generation
                generation = self.creation_nouvelle_generation(population)
            else : # sinon on dèmarre par la la generation prècèdente
                generation = self.creation_nouvelle_generation(generation)
                for i, solution in enumerate(generation): # partie d'èvalluation
                    generation[i] = self.solution_score(solution)

                generation = self.selectionGen(generation) # partie de Selection
                self.mutation(generation)

                generation = [solution['solution'] for solution in generation] # prendre seulement le champ "solution" de chaque dictionnaire de generation avant la prochaine iteration

                solution_optimale = generation[0] # la meilleure solution de la generation actuelle
                Solutions_optimales.append(solution_optimale)

        meilleure_solution = min(Solutions_optimales, key = lambda x:x)
        return meilleure_solution
    
    def best_route(self) :
        best_trajet = self.transform(self.best_solution())
        return best_trajet
    
    def create_graph(self) :
        trajet_v = self.best_route()
        arcs = []
        for trajet in trajet_v :
            for client in range(len(trajet) - 1) :
                arcs.append([trajet[client], trajet[client+1]])
        couleur_trajet = [
        'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
        'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'
        ]
        # Création du graphe dirigé
        graphe = nx.DiGraph()

        # Ajout des nœuds et des arêtes
        graphe.add_nodes_from(range(self.nb_client + 1))
        graphe.add_edges_from(arcs)

        # Dessin du graphe avec les positions fixes des nœuds
        plt.figure(figsize=(10, 6))

        # Définition des positions fixes des nœuds
        pos = nx.shell_layout(graphe)

        # Dessin des nœuds
        nx.draw_networkx_nodes(graphe, pos=pos, node_color='SkyBlue', node_size=1000)

        # Dessin des arcs
        for i in range(len(trajet_v)):
             arcs_trajet = []
             for client in range(len(trajet_v[i]) - 1):
                 arcs_trajet.append((trajet_v[i][client], trajet_v[i][client + 1]))
             nx.draw_networkx_edges(graphe, pos=pos, edgelist=arcs_trajet, edge_color=couleur_trajet[i], width=8, alpha=0.5)

        # Affichage des labels des nœuds 
        nx.draw_networkx_labels(graphe, pos=pos, font_size=15)

        plt.show()