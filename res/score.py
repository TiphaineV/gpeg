from contextRes import FastGraph, TrivialClf, ClfScorer
import numpy as np
import matplotlib.pyplot as plt

# Graph definition + classifier
graph = FastGraph()
clf = TrivialClf()
scorer = ClfScorer(graph)
metric = 0 # 0 for precision, 1 for recall, 2 for f1-score


def main():
    # -- Parameters
    nRecArr = range(1,21) # number of recommendation the recommender system should make
    alphaArr = [k/10 for k in range(1,10)] # test proportion in the split
    nLabelsArr = range(1,6) # number of labels for the classifier
    degreeExArr = range(1,6) # minimum degree of extracted labels

    #-- score array
    score = np.empty(shape = (9, 20, 5, 5))
    for alpha in alphaArr:
        trainEdges, testEdges = graph.train_test_split(alpha = alpha)

        # -- Fitting recommender system
        clf.fit(trainEdges)

        # -- Scoring
        for nRec in nRecArr:
            for nLabels in nLabelsArr:
                for degreeEx in degreeExArr:
                    score[int(10*alpha)-1, nRec-1, nLabels-1, degreeEx-1] = scorer.score(clf, testEdges, nRec, nLabels, degreeEx =degreeEx)[0]

    print('Best param: ', np.unravel_index(np.argmax(score), shape=(9, 20, 5, 5)))
    print('max: ', np.max(score))
    # -- figure definition
    fig, axes = plt.subplots(2,2, figsize = (10,8))
    
    # -- alpha dependancy
    axes[0,0].plot(alphaArr, score[:, 10, 3,2])
    axes[0,0].set_title('score = f(alpha)')

    # -- nRec dependancy
    axes[0,1].plot(nRecArr, score[8, :, 3,2])
    axes[0,1].set_title('score = f(nRec)')
    # -- nLabel dependancy
    axes[1,0].plot(nLabelsArr, score[8, 11, :,2])
    axes[1,0].set_title('score = f(nLabels)')

    # -- degreeEx dependancy
    axes[1,1].plot(degreeExArr, score[8,11,3,:])
    axes[1,1].set_title('score = f(dEx)')
    plt.show()


if __name__ == '__main__':
    main()

