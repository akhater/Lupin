# credits https://gist.github.com/doctorpangloss/13ab29abd087dc1927475e560f876797

def supermemo_2(x: [int], a=6.0, b=-0.8, c=0.28, d=0.02, assumed_score=2.5, min_score=1.3, theta=1.0) -> float:
    """
    Returns the number of days until seeing a problem again based on the 
    history of answers x to the problem, where the meaning of x is:
    x == 0: Incorrect, Hardest
    x == 1: Incorrect, Hard
    x == 2: Incorrect, Medium
    x == 3: Correct, Medium
    x == 4: Correct, Easy
    x == 5: Correct, Easiest
    @param x The history of answers in the above scoring.
    @param theta When larger, the delays for correct answers will increase.
    """
    assert all(0 <= x_i <= 5 for x_i in x)
    correct = [x_i >= 3 for x_i in x]
    # If you got the last question incorrect, just return 1
    if not correct[-1]:
        return 1.0
    
    # Calculate the latest consecutive answer streak
    r = 0
    for c_i in reversed(correct):
        if c_i:
            r+=1
        else:
            break
    
    return a*(max(min_score, assumed_score + sum(b+c*x_i+d*x_i*x_i for x_i in x)))**(theta*r)