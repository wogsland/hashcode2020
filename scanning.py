
files = ['a_example', 'b_read_on', 'c_incunabula', 'd_tough_choices', 'e_so_many_books', 'f_libraries_of_the_world']
bests = [17, 4126100, 828126, 7177170, 467865, 906706]


def read_libraries(filename):
    # read in file
    count = -2
    book_scores = []
    libraries = []
    number_of_books = 0
    number_of_libraries = 0
    number_of_days = 0
    library_books = 0
    library_days = 0
    library_per_day = 0
    for line in open(filename + '.txt', 'r'):
        # print(line)
        trunk = line.split('\n')
        pieces = trunk[0].split(' ')
        if len(pieces) == 1 and pieces[0] == '':
            continue
        if count == -2:
            number_of_books = int(pieces[0])
            number_of_libraries = int(pieces[1])
            number_of_days = int(pieces[2])
        elif count == -1:
            book_scores = pieces
        elif count % 2 == 0:
            #print(line)
            library_books = int(pieces[0])
            library_days = int(pieces[1])
            library_per_day = int(pieces[2])
        else:
            library = {
                "count": library_books,
                "signup_days": library_days,
                "per_day": library_per_day,
                "books": pieces,
            }
            libraries.append(library)
        count = count + 1

    score = 0
    libraries_signed_up = 0
    current = 0
    library_order = []
    books_at_library = 0
    books_already_scanned = [0] * len(book_scores)

    i = 0
    for library in libraries:
        #print("{} days to signup libraries".format(number_of_days))
        number_of_days = number_of_days - library["signup_days"]
        if number_of_days >= 0:
            libraries_signed_up = libraries_signed_up + 1
            #print("scanning books for library {}".format(i))
            new_score, new_books = scan_books(library["per_day"], library["books"], number_of_days, book_scores, books_already_scanned)
            score = score + new_score
            library_order.append({
                "id": i,
                "books": new_books
            })
        i = i + 1
    print("score {} for {}".format(score, filename))

    best = 0
    for i, name in enumerate(files):
        if name == filename:
            best = bests[i]
    if score > best:
        # write output file
        f = open(filename + ".out", "w")
        f.write("{}\n".format(libraries_signed_up))
        for library in library_order:
            f.write("{} {}\n".format(library["id"], len(library["books"])))
            #print()
            f.write(" ".join(library["books"]) + "\n")



def scan_books(books_per_day, books, days_left, book_scores, books_already_scanned):
    books_scanned = []
    score = 0
    book_index = 0
    for day in range(0, days_left):
        for book in range(0, books_per_day):
            #print("comparing {} < {}".format(book_index, len(books)))
            if book_index < len(books) and 0 == books_already_scanned[int(books[book_index])]:
                #print("day {}, book number {}".format(day, book_index))
                books_scanned.append(str(books[book_index]))
                score = score + int(book_scores[int(books[book_index])])
                books_already_scanned[int(books[book_index])] = 1
                book_index = book_index + 1
        if book_index == len(books):
            break
    return score, books_scanned


read_libraries(files[0])
#read_libraries(files[1])
#read_libraries(files[2])
#read_libraries(files[3])
#read_libraries(files[4])
#read_libraries(files[5])
