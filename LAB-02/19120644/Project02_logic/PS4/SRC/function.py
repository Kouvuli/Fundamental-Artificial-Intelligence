from copy import deepcopy

# check if 2 literals are complementary
def is_complementary(literal_1: str, literal_2: str):
    return len(literal_1) != len(literal_2) and literal_1[-1] == literal_2[-1]

# check if clause is valid
def is_valid(clause: list):
    for i in range(len(clause)-1):
        if is_complementary(clause[i],clause[i+1]):
            return True
    return False

# clause's literals alphabetically sorted
def alphabet_sort(literal: str):
    return ord(literal[-1])

# clear blank space and \n in clause
def clause_clear(clause: list):
    for i in range(len(clause)):
        clause[i] = clause[i].replace(' ', '')
        clause[i] = clause[i].replace('\n', '')

# clause negation suits CNF
def negate_clause(clause: list):
    neg_clause = []
    for i in range(len(clause)):
        if clause[i][0] != '-':
            neg_clause.append(list())
            neg_clause[-1].append('-'+clause[i])
        else:
            neg_clause.append(list())
            neg_clause[-1].append(clause[i][-1])

    return neg_clause

# format clause suits output request
def format_clause(clause: list):
    if (len(clause)==0):
        return '{}'

    formatted_clause = ''
    for i in range(len(clause) - 1):
        formatted_clause += clause[i] + ' OR '
    formatted_clause += clause[-1]

    return formatted_clause

# literal negation
def negate_literal(literal: str):
    if (len(literal)==1):
        return '-' + literal
    else:
        return str(literal[-1])

# resolve 2 clauses, put resolvent into container
def resolve(clause_1: list, clause_2: list, container: list):
    c1 = deepcopy(clause_1)
    c2 = deepcopy(clause_2)
    new_clause = None

    for i in range(len(c1)):
        neg_literal = negate_literal(c1[i])
        if neg_literal in c2:
            c1.remove(c1[i])
            c2.remove(neg_literal)
            new_clause = c1
            for j in range(len(c2)):
                if (c2[j] not in c1):
                    new_clause.append(c2[j])
            new_clause.sort(key=alphabet_sort)
            if not is_valid(new_clause) and new_clause not in container:
                container.append(new_clause)
            return
     
# check if clause_1 is a clause_2's subset
def is_subset(subset: list, superset: list):
    if len(subset)==0:
        return True
    for clause in subset:
        if clause not in superset:
            return False
    return True

# union clauses, result at the first one
def clauses_union(clauses_1: list, clauses_2: list):
    for clause in clauses_2:
        if clause not in clauses_1:
            clauses_1.append(clause)

# add new clauses to group
def grouping(clauses: list, group: list, main_clauses: list):
    new_clauses = deepcopy(clauses)
    i = 0
    while i < len(new_clauses):
        if new_clauses[i] in main_clauses:
            new_clauses.pop(i)
            i-= 1
        i+= 1
    
    group.append(new_clauses)

    

class PL_RESOLUTION:
    def __init__(self):
        self.alpha = []
        self.KB = []
        self.new_clauses_group = []
        self.result = False

    def read_file(self, input: str):
        f = open(input, 'r')
        self.alpha = f.readline().split('OR')
        clause_clear(self.alpha)

        for _ in range(int(f.readline())):
            self.KB.append(f.readline().split('OR'))
            clause_clear(self.KB[-1])

        f.close()

    def pl_resolution(self):
        clauses = deepcopy(self.KB)
        clauses += negate_clause(self.alpha)

        while True:
            nClause = len(clauses)   # number of clause
            new_clauses = []
            for i in range(nClause):
                for j in range(i+1, nClause):
                    resolve(clauses[i], clauses[j], new_clauses)

            grouping(new_clauses, self.new_clauses_group, clauses)
            if list() in new_clauses:
                self.result = True
                return
            if is_subset(new_clauses, clauses):
                return
            clauses_union(clauses, new_clauses)
            
    def write_file(self, output: str):
        f = open(output, 'w')

        for new_clauses in self.new_clauses_group:
            f.write(str(len(new_clauses)) + '\n')
            for clause in new_clauses:
                f.write(format_clause(clause) + '\n')

        if self.result == True:
            f.write('YES')
        else:
            f.write('NO')

        f.close()
