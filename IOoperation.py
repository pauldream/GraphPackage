import xlrd #, xlsxwriter


# # Function for writing distance into excel file, distance is two dimensional dictionary
# def write_distance(filename, sheet, distance):
#     book = xlsxwriter.Workbook(filename + '.xlsx')
#     sh = book.add_worksheet(sheet)
#     bold = book.add_format({'bold': True})
#     sh.write(0, 0, 'Start', bold)
#     sh.write(0, 1, 'End', bold)
#     sh.write(0, 2, 'Distance', bold)
#     count_row = 1
#     for i in distance.keys():
#         for j in xrange(len(distance[i].keys())):
#             sh.write(count_row, 0, i)
#             sh.write(count_row, 1, distance[i].keys()[j])
#             sh.write(count_row, 2, distance[i][distance[i].keys()[j]])
#             count_row = count_row + 1
#     book.close()


def read_link(filename, sheet, num_link):
    """reading link information into link list, each element is [ori index, des index, length]

    """
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name(sheet)
    # sheet = book.sheet_by_index(0) # Open the first sheet in the book
    origin = sheet.col_values(1,1,num_link+1)
    destination = sheet.col_values(2,1,num_link+1)
    length = sheet.col_values(3,1,num_link+1)
    link = []
    for i in xrange(num_link):
        link.append([str(origin[i]), str(destination[i]), length[i]])
    return link


def read_node(filename, sheet, num_node):
    """reading node information into node list, each element is [node index, x-coor, y-coor]

    """
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name(sheet)
    index = sheet.col_values(0,1,num_node+1)
    x_coor = sheet.col_values(1,1,num_node+1)
    y_coor = sheet.col_values(2,1,num_node+1)
    node = []
    for i in xrange(num_node):
        node.append([str(index[i]), x_coor[i], y_coor[i]])
    return node

