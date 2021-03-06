#!/usr/bin/python

# A quick and dirty script generate review reports

import csv
import os
import sys
import time

proposals = {}
for row in csv.DictReader(open('allproposals.csv'), delimiter=';'):
    proposals[row['proposal_id']] = row

reviews = {}
for row in csv.DictReader(open('allreviews.csv'), delimiter=';'):
    reviews.setdefault(row['id'], [])
    reviews[row['id']].append(row)

scores = {}
likely_accept = []
likely_reject = []

for proposal_id in proposals:
    if (proposals[proposal_id]['type'] != 'Miniconf' and
        proposals[proposal_id]['name'] != 'Withdrawn'):

        score_details = []
        int_scores = []
        total = 0
        count = 0
        for review in reviews[proposal_id]:
            score = review['score']
            if len(score) == 0:
                score = '*'
            else:
                int_score = int(score)
                total += int_score
                count += 1
                int_scores.append(int_score)

            score_details.append('    %2d ... %s %s' %(int_score,
                                                       review['firstname'],
                                                       review['lastname']))

        score_details.append('    --------------------------------')
        score = float(total) / float(count)
        score_details.append('    Score %.02f' % score)

        s = '    '
        int_scores.sort()
        median = len(int_scores) / 2
        count = 0
        for int_score in int_scores:
            s += '%d ' % int_score
            if count == median:
                s += '* '
            count += 1
        score_details.append(s)

        scores[proposal_id] = score_details
        
        if score > 1.50:
            likely_accept.append(proposal_id)

        if score < 0.00:
            new_total = 0
            for s in int_scores[2:]:
                new_total += s
            new_score = float(new_total) / (len(int_scores) - 2)
            if new_score < 0.00:
                likely_reject.append(proposal_id)

for n, p in [("Likely accept", likely_accept),
             ("Likely reject", likely_reject)]:
    print '=' * 80
    print n
    print '=' * 80

    for proposal_id in p:
        print '%s: %s (%s %s)' %(proposal_id,
                                 proposals[proposal_id]['title'],
                                 proposals[proposal_id]['firstname'],
                                 proposals[proposal_id]['lastname'])
        print '\n'.join(scores[proposal_id][-2:])
        print

    print
    print
