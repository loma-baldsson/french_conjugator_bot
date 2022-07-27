import itertools

EDGE_MARKER = "!"
CORNER_MARKER = "."

TABLE_CHARS = [
    ["┌", "┬", "┐"],
    ["├", "┼", "┤"],
    ["└", "┴", "┘"],
    ["─", "│"]
]

def validate_table(table):
    assert type(table) == list, "'table' is not type list"
    assert len(table) != 0, "'table' is empty"

    row_length = len(table[0])
    
    for row in table:
        assert type(row) == list, "Not all rows are lists"
        assert len(row) != 0, "Some rows are empty!"
        
        for cell in row:
            assert type(cell) == str, "Not all cells are strings"

        assert len(row) == row_length, "Not all rows are the same length"


def get_col_widths(table):
    col_widths = []
    for col_index in range(len(table[0])):
        col_widths.append(max([len(row[col_index]) for row in table]) + 2)

    return col_widths


def create_template_table(table):
    new_table = []
    
    for i in range(2*len(table) + 1):
        new_row = []
        for j in range(2*len(table[0]) + 1):
            new_row.append(EDGE_MARKER)

        new_table.append(new_row)

    for i in range(0, len(new_table), 2):
        for j in range(0, len(new_table[0]), 2):
            new_table[i][j] = CORNER_MARKER
    
    for i in range(len(table)):
        for j in range(len(table[0])):
            new_table[i*2 + 1][j*2 + 1] = table[i][j]
    
    return new_table


def render_corner(x, y, table_height, table_width, col_widths):
    assert x <= table_height-1, "X value is bigger than table_height"
    assert y <= table_width-1, "Y value is bigger than table height"
    assert x % 2 == 0 and y % 2 == 0, "Not a corner"
    
    if x == 0:
        if y == 0:
            return TABLE_CHARS[0][0]
        elif y == table_width - 1:
            return TABLE_CHARS[0][2]
        else:
            return TABLE_CHARS[0][1]

    if x == table_height - 1:
        if y == 0:
            return TABLE_CHARS[2][0]
        elif y == table_width - 1:
            return TABLE_CHARS[2][2]
        else:
            return TABLE_CHARS[2][1]

    if y == 0:
        return TABLE_CHARS[1][0]
    elif y == table_width - 1:
        return TABLE_CHARS[1][2]
    else:
        return TABLE_CHARS[1][1]


def render_edge(x, y, table_height, table_width, col_widths):
    assert x % 2 == 0 or y % 2 == 0, "Not an edge"
    assert not (x % 2 == 0 and y % 2 == 0), "Not an edge, but a corner"
    
    if x % 2 == 0:
        return TABLE_CHARS[3][0] * col_widths[y]
    elif y % 2 == 0:
        return TABLE_CHARS[3][1]


def render_string(x, y, table_height, table_width, col_widths, text):
    return " " + text.ljust(col_widths[y]-1)


def render_table(table, render_corner=render_corner, render_edge=render_edge, render_string=render_string):
    template_table = create_template_table(table)
    col_widths = get_col_widths(template_table)
    
    table_height = len(template_table)
    table_width = len(template_table[0])

    output = ""
    
    for i in range(len(template_table)):
        for j in range(len(template_table[0])):
            if template_table[i][j] == CORNER_MARKER:
                output += render_corner(i, j, table_height, table_width, col_widths)
            elif template_table[i][j] == EDGE_MARKER:
                output += render_edge(i, j, table_height, table_width, col_widths)
            else:
                output += render_string(i, j, table_height, table_width, col_widths, template_table[i][j])
            
        output += "\n"

    return output.strip()

def pad_table(table):
    length = 0

    for row in table.split("\n"):
        length = max(length, len(row))

    output = ""

    for row in table.split("\n"):
        output += row.ljust(length)
        output += "\n"

    return output

def join_tables(*tables, padding=2):
    assert type(padding) == int, "padding isn't type int"
    
    split_tables = []
    
    for table in tables:
        assert type(table) == str, "Not all tables are strings!"
        
        rows = []
        for row in table.split("\n"):
            rows.append(row + padding*" ")
            
        split_tables.append(rows)

    output = ""
    for row in itertools.zip_longest(*split_tables):
        output += "".join(row) + "\n"

    return output.strip()
    
if __name__ == "__main__":
    table = [
        ["The", "quick", "brown"], 
        ["fox", "jumps", "over"], 
        ["the", "lazy", "dog"]
    ]

    rendered_table = render_table(table)
    
    print(render_table(table))
    print(join_tables(rendered_table, rendered_table))