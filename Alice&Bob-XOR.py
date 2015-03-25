__author__ = 'Krishna'


def byte(string):
    return [ord(i)  for i in string]

def make_word(byte):
    chars = [chr(i) for i in byte]
    return "".join(chars)

def xor(input1, input2):
    return [i ^ j for i, j in zip(input1,input2)]

def disp_bin(int_list):
    return [format(i, '#010b') for i in int_list]

def speak(Bob_Data, Alice_Data, XOR_ENCODING):
    """
    This function simulates a simple exchange of data between Bob and Alice with and without XOR encoding
    and measures the number of time-slots taken to transfer the msg.
    :param Bob_Data: Data sent by Bob to Alice
    :param Alice_Data: Data sent by Alice to Bob
    :param XOR_ENCODING: True if data to be transmitted using XOR encoding
    :return:
    """
    if XOR_ENCODING:
        print "\n######## Relay WITH Encoding ########\n"
    else:
        print "\n######## Relay WITHOUT Encoding ########\n"

    used_time_slots = 0

    bob_tx = Bob_Data
    used_time_slots += 1
    print "Bob transmits : ", bob_tx

    alice_tx = Alice_Data
    used_time_slots +=1
    print "Alice transmits : ", alice_tx


    if XOR_ENCODING:
        byte_bob = byte(bob_tx)
        print "\nBob_tx serialised   : ", disp_bin(byte_bob)

        byte_alice = byte(alice_tx)
        print "Alice_tx serialised : ", disp_bin(byte_alice)

        print "\nEncoding..."
        rel_encodedTx = xor(byte_bob, byte_alice)
        used_time_slots +=1
        print "Relay - Encoded Tx  : ", disp_bin(rel_encodedTx)


        bob_rx = rel_encodedTx
        print "\nBob recieves        : ", disp_bin(rel_encodedTx)
        alice_rx = rel_encodedTx
        print "Alice recieves      : ", disp_bin(rel_encodedTx)

        print "\nDecoding..."
        bob_decoded = make_word(xor(byte_bob, rel_encodedTx))
        alice_decoded = make_word(xor(byte_alice, rel_encodedTx))

        print "Bob decoded   : ", bob_decoded
        print "Alice decoded : ", alice_decoded


    else:

        print "\nRelay simply exchanges the msgs individually"
        bob_rx = alice_tx
        used_time_slots +=1
        print "\nBob recieves   : ", bob_rx

        alice_rx = bob_tx
        used_time_slots +=1
        print "Alice recieves   : ", alice_rx

    print "\n\t\t##################\nNUMBER OF TIME SLOTS USED TO TRANSMIT MSG : ", used_time_slots



speak("Hello", "World", True)


