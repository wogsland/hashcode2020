import math
files = ['a_example', 'b_read_on', 'c_incunabula', 'd_tough_choices', 'e_so_many_books', 'f_libraries_of_the_world']
bests = [21, 5822900, 5467966, 4871555, 3383088, 5212833]
# bests = [0,0,0,0,0,0]


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
    library_count = 0
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
            weight = library_weight(pieces, book_scores, library_days, library_per_day)
            library = {
                "id": library_count,
                "count": library_books,
                "signup_days": library_days,
                "per_day": library_per_day,
                "books": pieces,
                "weight": weight,
            }
            libraries.append(library)
            library_count = library_count + 1
        count = count + 1

    score = 0
    libraries_signed_up = 0
    current = 0
    library_order = []
    books_at_library = 0
    books_already_scanned = [0] * len(book_scores)

    libraries = sort_libraries(libraries)
    for library in libraries:
        #print("{} days to signup libraries".format(number_of_days))
        number_of_days = number_of_days - library["signup_days"]
        if number_of_days >= 0:
            #print("scanning books for library {}".format(i))
            new_score, new_books, new_books_already_scanned = scan_books(library["per_day"], library["books"], number_of_days, book_scores, books_already_scanned)
            if new_score > 0:
                score = score + new_score
                libraries_signed_up = libraries_signed_up + 1
                library_order.append({
                    "id": library["id"],
                    "books": new_books
                })
                books_already_scanned = new_books_already_scanned
            else:
                number_of_days = number_of_days + library["signup_days"]

    best = 0
    for i, name in enumerate(files):
        if name == filename:
            best = bests[i]
    print("score {} for {}".format(score, filename))
    print("prior best {} for {}".format(best, filename))
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
            #if book_index < len(books) and 0 == books_already_scanned[int(books[book_index])]:
            while book_index < len(books) and 1 == books_already_scanned[int(books[book_index])]:
                book_index = book_index + 1
            if book_index < len(books):
                #print("day {}, book number {}".format(day, book_index))
                books_scanned.append(str(books[book_index]))
                score = score + int(book_scores[int(books[book_index])])
                books_already_scanned[int(books[book_index])] = 1
                book_index = book_index + 1
        if book_index == len(books):
            break
    return score, books_scanned, books_already_scanned


def sort_libraries(libraries):
    print("sorting libraries")
    libraries = sorted(libraries, key=lambda library: library["weight"], reverse=True)
    #libraries = sorted(libraries, key=lambda library: library["signup_days"])
    return libraries


def library_weight(books, book_scores, signup_days, library_per_day):
    weight = 0
    for book in books:
        weight = weight + int(book_scores[int(book)])
    if signup_days == 0:
        return 999999999999999999
    else:
        return (weight/signup_days)*math.sqrt(library_per_day)


read_libraries(files[0])
read_libraries(files[1])
read_libraries(files[2])
read_libraries(files[3])
read_libraries(files[4])
read_libraries(files[5])
