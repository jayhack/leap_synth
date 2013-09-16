#!/opt/local/bin/python
import numpy as np

class HMM_Backend:


    follow_prob = None
    startprob = None


    def get_startprob (self, sequences, num_states):
        self.startprob = np.zeros((num_states))
        for sequence in sequences:
            start_state = sequence[0]
            self.startprob[start_state] += 1
        total = float(sum(self.startprob))
        for index, t in enumerate(self.startprob):
            self.startprob[index] /= total

        print "----- START PROB -----"
        print self.startprob


    def init_follow_prob (self, num_states):

        self.follow_prob = np.zeros ((num_states, num_states))
        print "----- INITIALIZED FOLLOW PROB -----"
        print self.follow_prob


    # Function: get_follow_counts
    # ---------------------------
    # fills follow_counts
    def get_follow_counts (self, sequences):

        for sequence in sequences:
            for index, entry in enumerate(sequence[:-1]):

                prev = entry 
                next = sequence[index + 1]

                self.follow_prob [prev][next] += 1.0

        print "----- FOLLOW PROB UNNORMALIZED -----"
        print self.follow_prob


    # Function: get_follow_probs
    # --------------------------
    # fills follow_prob
    def get_follow_probs (self):

        for index1, row in enumerate(self.follow_prob):
            total = sum(row)
            if total != 0:
                for index2, element in enumerate(self.follow_prob[index1]):
                    self.follow_prob[index1][index2] /= total

        print "--- Final Follow Prob ---"
        print self.follow_prob


    def __init__(self, sequences, num_states):

        self.get_startprob(sequences, num_states)
        self.init_follow_prob (num_states)
        self.get_follow_counts (sequences)
        self.get_follow_probs ()



    def get_prob (self, sequence):
        total_prob = 1
        for index, entry in enumerate(sequence[:-1]):

            prev = entry - 1
            next = sequence[index + 1] - 1
            total_prob *= self.follow_prob[prev][next]
        return total_prob



if __name__ == "__main__":


    s1 = [1, 2, 3]
    s2 = [1, 4, 3]
    num_states = 4
    h = HMM_Backend ([s1, s2], num_states)

    print h.get_prob ([4, 1, 2])