import copy

class WorldCupCSP:
    def __init__(self, teams, groups, debug=False):
        """
        Inicializa el problema CSP para el sorteo del Mundial.
        :param teams: Diccionario con los equipos, sus confederaciones y bombos.
        :param groups: Lista con los nombres de los grupos (A-L).
        :param debug: Booleano para activar trazas de depuración.
        """
        self.teams = teams
        self.groups = groups
        self.debug = debug

        # Las variables son los equipos.
        self.variables = list(teams.keys())

        # El dominio de cada variable inicialmente son todos los grupos.
        self.domains = {team: list(groups) for team in self.variables}

    def get_team_confederation(self, team):
        return self.teams[team]["conf"]

    def get_team_pot(self, team):
        return self.teams[team]["pot"]

    def is_valid_assignment(self, group, team, assignment):

        # tamaño grupo
        if list(assignment.values()).count(group) >= 4:
            return False

        team_pot = self.get_team_pot(team)
        team_conf = self.get_team_confederation(team)

        conf_count = 0
        uefa_count = 0

        for t, g in assignment.items():

            if g != group:
                continue

            # no repetir bombo
            if self.get_team_pot(t) == team_pot:
                return False

            conf = self.get_team_confederation(t)

            if conf == team_conf:
                conf_count += 1

            if conf == "UEFA":
                uefa_count += 1

        if team_conf == "UEFA":
            if uefa_count >= 2:
                return False
        else:
            if conf_count >= 1:
                return False

        return True

    def forward_check(self, assignment, domains):

        new_domains = copy.deepcopy(domains)

        for var in new_domains.keys():

            if var in assignment:
                continue

            valid_groups = []

            for group in new_domains[var]:

                if self.is_valid_assignment(group, var, assignment):
                    valid_groups.append(group)

            new_domains[var] = valid_groups

            if len(valid_groups) == 0:
                return False, new_domains

        return True, new_domains

    def select_unassigned_variable(self, assignment, domains):

        unassigned = [v for v in domains.keys() if v not in assignment]

        if not unassigned:
            return None

        return min(unassigned, key=lambda var: len(domains[var]))

    def backtrack(self, assignment, domains=None):

        if domains is None:
            domains = copy.deepcopy(self.domains)

        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment, domains)

        for group in domains[var]:

            if self.is_valid_assignment(group, var, assignment):

                assignment[var] = group

                success, new_domains = self.forward_check(assignment, domains)

                if success:
                    result = self.backtrack(assignment, new_domains)
                    if result is not None:
                        return result

                del assignment[var]

        return None
