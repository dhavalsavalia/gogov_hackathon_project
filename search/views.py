from django.shortcuts import render
from haystack.query import SearchQuerySet

def testpage(request):
    test_results = SearchQuerySet().auto_query('SOlr')
    spelling_suggestion = test_results.spelling_suggestion()

    # final_spelling = spelling_suggestion.split("(")
    # final_two_spelling = final_spelling[1].split(")")

    return render(request, 'testpage.html', {   
        'spelling_suggestion': spelling_suggestion, 
    })
