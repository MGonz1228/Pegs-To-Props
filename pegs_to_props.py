time = 1
pegs_list = []
jumps_list = []

def write_propositions_to_output(jumps_list, pegs_list):
    with open('my_propositions.txt', 'w') as output_file: 
        output_file.write('Lists are Jumps, tuples are Pegs\n')
        for i in range(1, (len(jumps_list)+len(pegs_list) + 1)):
            if i < len(jumps_list)+1:
                line = [str(i) + ' ', str(jumps_list[i-1]) + '\n']
                output_file.writelines(line)
            else:
                line = [str(i) + ' ' , str(pegs_list[i-len(jumps_list)-1]) + '\n']
                output_file.writelines(line)

def get_pegs(triples, max_time):
    for triple in triples:
        for time in range(1, max_time + 1):
            pegs_list.append((triple[0],time))

    return pegs_list

def get_jumps(triples, max_time):
    for triple in triples:
        for time in range(1, max_time):
            jumps_list.append([*triple, time])
        for time in range(1, max_time):
            jumps_list.append([*triple[::-1], time])

    return jumps_list

def file_contents_to_lists(file_jumps, file_pegs):
    actual_jumps = []
    actual_pegs = []

    for jump in file_jumps:
        this_jump = []
        index = int(jump[0])
        jump_len = len(jump)
        for i in range(1, jump_len):
            this_jump.append(int(jump[i].replace('[','').replace(',','').replace(']','')))
        actual_jumps.append([index, this_jump])

    for peg in file_pegs:
        this_peg = []
        index = int(peg[0])
        peg_len = len(peg)
        for i in range(1, peg_len):
            this_peg.append(int(peg[i].replace('(','').replace(',','').replace(')','')))
        actual_pegs.append([index, this_peg])

    return(actual_jumps, actual_pegs)

def read_propositions(jumps_list):
    file_pegs = []
    file_jumps = []
    jumps_count = len(jumps_list)
    with open('my_propositions.txt', 'r') as input_file:
        for line in input_file.readlines()[1:]:
            line = line.strip().split()
            if int(line[0]) <= jumps_count:
                file_jumps.append(line)
            else:
                file_pegs.append(line)

    propositions = file_contents_to_lists(file_jumps, file_pegs)
    return propositions

def encode_preconditions(jumps, pegs):
    # determine pegs required for a jump
    # Jump(A,B,C,TIME) => Peg(A,TIME) ∧ Peg(B,TIME) ∧ ¬Peg(C,TIME)

    output_file = open('my_output.txt', 'w') 
    for jump in jumps:
        jump_index = jump[0]
        jump_action = jump[1]
        jump_A = jump_action[0]
        jump_B = jump_action[1]
        jump_C = jump_action[2]
        jump_time = jump_action[3]
        current_clause = str(jump_index - 2*jump_index) + ' '

        for peg in pegs:
            peg_index = str(peg[0])
            peg_info = peg[1]
            peg_number = peg_info[0]
            peg_time = peg_info[1]

            if jump_time == peg_time:
                if jump_A == peg_number:
                    current_clause += peg_index + '\n'
                    output_file.write(current_clause)
                    current_clause = str(jump_index - 2*jump_index) + ' '
                if jump_B == peg_number:
                    current_clause += peg_index + '\n'
                    output_file.write(current_clause)
                    current_clause = str(jump_index - 2*jump_index) + ' '
                if jump_C == peg_number:
                    current_clause += str(int(peg_index) - 2*int(peg_index)) + '\n'
                    output_file.write(current_clause)
                    current_clause = str(jump_index - 2*jump_index) + ' '

    output_file.close()


def encode_causals(jumps, pegs):
    # determine pegs of time+1 that are mutually exclusive with that jump
    # Jump(A,B,C,TIME) => ¬Peg(A,TIME+1) ∧ ¬Peg(B,TIME+1) ∧ Peg(C,TIME+1)

    output_file = open('my_output.txt', 'a') 
    for jump in jumps:
        jump_index = jump[0]
        jump_action = jump[1]
        jump_A = jump_action[0]
        jump_B = jump_action[1]
        jump_C = jump_action[2]
        jump_time = jump_action[3]
        current_clause = str(jump_index - 2*jump_index) + ' '

        for peg in pegs:
            peg_index = str(peg[0])
            peg_info = peg[1]
            peg_number = peg_info[0]
            peg_time = peg_info[1]
    
            if jump_time + 1 == peg_time:
                if jump_A == peg_number:
                    current_clause += str(int(peg_index) - 2*int(peg_index)) + '\n'
                    output_file.write(current_clause)
                    current_clause = str(jump_index - 2*jump_index) + ' '
                if jump_B == peg_number:
                    current_clause += str(int(peg_index) - 2*int(peg_index)) + '\n'
                    output_file.write(current_clause)
                    current_clause = str(jump_index - 2*jump_index) + ' '
                if jump_C == peg_number:
                    current_clause += peg_index + '\n'
                    output_file.write(current_clause)
                    current_clause = str(jump_index - 2*jump_index) + ' '

    output_file.close()

def encode_frames(jumps, pegs, max_time):
    # Peg(N,TIME) ∧ ¬Peg(N,TIME+1) => Jump(A,N,C,TIME) ∨ Jump(C,N,A,TIME) ∨ Jump(N,B,C,TIME) ∨ Jump(N,C,B,TIME) 
        # N was Jump(B) at time TIME, or N was Jump(A) at time TIME
            # clause = neg index of peg
            # clause += index of peg(TIME+1)
            # clause += all jumps where peg_num is in slot A or B

    output_file = open('my_output.txt', 'a') 
    for peg in pegs:
        peg_index = str(peg[0])
        peg_info = peg[1]
        peg_number = peg_info[0]
        peg_time = peg_info[1]
        if peg_time == max_time:
            continue
        current_clause = str(int(peg_index) - 2*int(peg_index)) + ' '

        for compare_peg in pegs:
            compare_peg_index = str(compare_peg[0])
            compare_peg_info = compare_peg[1]
            compare_peg_number = compare_peg_info[0]
            compare_peg_time = compare_peg_info[1]

            if compare_peg_number == peg_number and compare_peg_time == peg_time + 1:
                current_clause += compare_peg_index + ' '

        for jump in jumps:
            jump_index = jump[0]
            jump_action = jump[1]
            jump_A = jump_action[0]
            jump_B = jump_action[1]
            jump_C = jump_action[2]
            jump_time = jump_action[3]
                
            if jump_A == peg_number or jump_B == peg_number:
                if jump_time == peg_time:
                    current_clause += str(jump_index) + ' '

        output_file.write(current_clause[:-1] + '\n')

    # ¬Peg(N,TIME) ∧ Peg(N,TIME+1) => Jump(A,B,N,TIME) ∨ 
        # N was Jump(C) at time TIME
            # clause = peg index
            # clause += neg index(peg(TIME+1))
            # clause += all jumps where peg_num is in slot C

    for peg in pegs:
        peg_index = str(peg[0])
        peg_info = peg[1]
        peg_number = peg_info[0]
        peg_time = peg_info[1]
        if peg_time == max_time:
            continue
        current_clause = peg_index + ' '

        for compare_peg in pegs:
            compare_peg_index = str(compare_peg[0])
            compare_peg_info = compare_peg[1]
            compare_peg_number = compare_peg_info[0]
            compare_peg_time = compare_peg_info[1]

            if compare_peg_number == peg_number and compare_peg_time == peg_time + 1:
                current_clause += str(int(compare_peg_index) - 2*int(compare_peg_index)) + ' '

        for jump in jumps:
            jump_index = jump[0]
            jump_action = jump[1]
            jump_A = jump_action[0]
            jump_B = jump_action[1]
            jump_C = jump_action[2]
            jump_time = jump_action[3]
                
            if jump_C == peg_number:
                if jump_time == peg_time:
                    current_clause += str(jump_index) + ' '

        output_file.write(current_clause[:-1] + '\n')
    output_file.close()

def encode_one_actions(jumps):
    # for jump
        # append neg jump index
            # for jump
                # if times match
                    # append neg jump
                # if clause changed and not dupe
                    # write

    output_file = open('my_output.txt', 'a')
    for jump in jumps:
        jump_index = jump[0]
        jump_action = jump[1]
        jump_time = jump_action[3]
        current_clause = str(jump_index - 2*jump_index) + ' '

        for compare_jump in jumps:
            current_clause = str(jump_index - 2*jump_index) + ' '
            compare_jump_index = compare_jump[0]
            compare_jump_action = compare_jump[1]
            compare_jump_time = compare_jump_action[3]
            
            if compare_jump_time == jump_time and compare_jump_index != jump_index:
                current_clause += str(compare_jump_index - 2*compare_jump_index) + '\n'

            if current_clause != str(jump_index - 2*jump_index) + ' ' and int(jump_index) < int(compare_jump_index):
                output_file.write(current_clause) 
    output_file.close()
            
def encode_start_state(empty_hole, pegs):
    output_file = open('my_output.txt', 'a')

    for peg in pegs:
        peg_index = str(peg[0])
        peg_info = peg[1]
        peg_number = peg_info[0]
        peg_time = peg_info[1]

        if peg_time == 1:
            if peg_number == empty_hole:
                current_clause = str(int(peg_index) - 2*int(peg_index)) + '\n'
                output_file.write(current_clause)
            else:
                current_clause = peg_index + '\n'
                output_file.write(current_clause)

    output_file.close()

def encode_end_state(pegs, max_time, num_holes):
    # At least one peg remains at time max_time
        # Peg(1, max_time) ... Peg(num_holes, max_time) 

    output_file = open('my_output.txt', 'a')
    current_clause = ''
    for peg in pegs:
        peg_index = str(peg[0])
        peg_info = peg[1]
        peg_time = peg_info[1]

        if peg_time == max_time:
            current_clause += peg_index + ' '

    output_file.write(current_clause[:-1] + '\n')

    # No two holes have a peg
    # for peg at time 3
        # for non self peg at time 3
            # if index increase
                # write both neg pegs
        
    for peg in pegs:
        peg_index = str(peg[0])
        peg_info = peg[1]
        peg_number = peg_info[0]
        peg_time = peg_info[1]
        current_clause = str(int(peg_index) - 2*int(peg_index)) + ' '
        
        if peg_time == max_time:
            for compare_peg in pegs:
                current_clause = str(int(peg_index) - 2*int(peg_index)) + ' '
                compare_peg_index = str(compare_peg[0])
                compare_peg_info = compare_peg[1]
                compare_peg_number = compare_peg_info[0]
                compare_peg_time = compare_peg_info[1]
                
                if compare_peg_time == max_time and compare_peg_index != peg_index:
                    if peg_index < compare_peg_index:
                        current_clause += str(int(compare_peg_index) - 2*int(compare_peg_index)) + '\n'
                        output_file.write(current_clause)
    output_file.close()

def triples_to_logic(num_holes, empty_hole, triples):
    max_time = num_holes - 1 
    pegs_list = get_pegs(triples, max_time)
    jumps_list = get_jumps(triples, max_time) 
    write_propositions_to_output(jumps_list, pegs_list)

    props = read_propositions(jumps_list)
    jumps = props[0]
    pegs = props[1]

    encode_preconditions(jumps, pegs)
    encode_causals(jumps, pegs)
    encode_frames(jumps, pegs, max_time)
    encode_one_actions(jumps)
    encode_start_state(empty_hole, pegs)
    encode_end_state(pegs, max_time, num_holes)

#    print(*jumps, sep='\n', end='\n\n')
#    print(*pegs, sep='\n')

def open_file(filename):
    try:
        input_file = open(filename, 'r')
        input_lines = input_file.readlines()
    except:
        print('Failed to open file: ', filename)
        exit(1)

    return [input_lines[0].strip().split(), list(map(lambda l: l.strip().split(), input_lines[1:]))]

def main():
    contents = open_file('input.txt')
    num_holes = int(contents[0][0])
    empty_hole = int(contents[0][1])
    triples = [[int(num) for num in lst] for lst in contents[1]]
    triples_to_logic(num_holes, empty_hole, triples)
    print('Check files \'my_output.txt\' and \'my_propositions.txt\' for output.')

if __name__ == '__main__':
    main()
