import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            for str_ in self.domains[var].copy():
                if var.length!=len(str_):
                    self.domains[var].remove(str_)
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        bool_=False
        if self.crossword.overlaps[x,y]:
            for str_x in self.domains[x].copy():
                bool__=False
                for str_y in self.domains[y].copy():
                    #print(f"{str_x}:{str_y}",f"{str_x[self.crossword.overlaps[x,y][0]]}:{str_y[self.crossword.overlaps[x,y][1]]}")
                    if str_x[self.crossword.overlaps[x,y][0]] \
                    ==str_y[self.crossword.overlaps[x,y][1]]:
                        bool__=True
                if not bool__:
                    self.domains[x].remove(str_x)
                    bool_=True
        return bool_
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs==None:
            arcs=list(self.crossword.overlaps.keys())
        for arc in arcs:
            if self.crossword.overlaps[arc]:
                #print(" #s ",self.crossword.overlaps[arc])
                #print(" #  ",set( map(  lambda s:s[self.crossword.overlaps[arc][0]],self.domains[arc[0]] ) ) )
                #print(" #  ",set( map(  lambda s:s[self.crossword.overlaps[arc][1]],self.domains[arc[1]] ) ) )
                bool_=self.revise(arc[0],arc[1])
                if len(self.domains[arc[0]])<=0:
                    return False
                elif bool_:
                    arcs.append(arc)
        return True
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment or len(assignment[var])!=1:
                return False
        return True
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        set_=set()
        for var in assignment:
            set_.add(assignment[var])
            if var.length!=len(assignment[var]):
                return False
            for var_ in assignment:
                if var!=var_ and self.crossword.overlaps[var,var_]!=None \
                and assignment[var][self.crossword.overlaps[var,var_][0]] \
                !=assignment[var_][self.crossword.overlaps[var,var_][1]]:
                    return False
        if len(set_) < len(assignment):
            return False
        return True
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        list_=[]
        for var_ in self.crossword.variables():
            count_=0
            if self.crossword.overlaps[var,var_]!=None:
                for str_ in self.domains[var_]:
                    if assignment[var][self.crossword.overlaps[var,var_][0]]!=str_[self.crossword.overlaps[var,var_][1]] and str_!=assignment[var_]:
                        count_+=1
            list_.append((var_,count_))
        return list(map(lambda v:v[0] ,sorted(list_,key=lambda li:li[1])))
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        list_=sorted(list(map(lambda v:(v[0],len(v[1])),self.domains.items())),key=lambda li:li[1])
        fewest_=None
        for cell_ in list_[::-1]:
            if cell_[0] not in assignment:
                fewest_=cell_
                break
        #lllll=[]
        for cell_ in list_:
            if cell_[0] not in assignment:
                #lllll.append(cell_[0])
                if fewest_[1]>cell_[1]:
                    fewest_=cell_
                elif fewest_[1]==cell_[1] and fewest_!=cell_:
                    for var_ in self.domains:
                        count_f=0
                        count_c=0
                        if var_!=fewest_[0] and self.crossword.overlaps[fewest_[0],var_]!=None:
                            count_f+=1
                        if var_!=cell_[0] and self.crossword.overlaps[cell_[0],var_]!=None:
                            count_c+=1
                    if count_f<=count_c:
                        fewest_=cell_
                else:
                    break
        #print(lllll)
        return fewest_[0]
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        # print(len(assignment),len(self.crossword.variables))
        if len(assignment) == len(self.crossword.variables):
            return assignment
         # Try a new str_
        var = self.select_unassigned_variable(assignment)
        for str_ in list(self.domains[var]):
            new_assignment = assignment.copy()
            new_assignment[var] = str_

            # ac3
            """
            list_=[]
            for var_ in self.crossword.variables:
                if (var_,var) in self.crossword.overlaps.keys():
                    list_.append((var_,var))
            self.ac3(list_)
            """
            #print(f"{len(new_assignment)}/{len(self.crossword.variables)}",new_assignment)
            #print(new_assignment)
            """
            print(assignment)
            print(new_assignment)
            print(len(assignment),"vs",len(new_assignment))
            print("-----------------------")
            if len(new_assignment)==len(assignment):
                print("WHY?")
                break
            """
            #print(len(new_assignment),self.domains[var],str_)
            #print(var,str_)
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
            #print(f"{len(new_assignment)}/{len(self.crossword.variables)}",new_assignment)
        return None
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
