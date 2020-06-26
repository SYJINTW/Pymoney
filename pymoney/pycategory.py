#!/usr/bin/env python3
import sys

#class
#=======================================================================================
class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense',['food', ['meal', 'snack', 'drink'], 'transport', ['bus', 'railway']], 'income', ['salary', 'bonus'], 'unknown']
        
    def user_view_categories(self, categories, prefix = ()):
        if type(categories) in {list,tuple}:
            i = 0
            for child in categories:
                if type(categories) not in {list,tuple}:
                    i += 1
                self.user_view_categories(child, prefix + (i,))
        else:
            print(' '*4*(len(prefix)-1) + '-' + categories)

    def is_category_valid(self, category, categories):
        if type(categories) == list:
            for child in categories:
                if self.is_category_valid(category, child):
                    return True
        else:
            return category == categories
        return False

    def find_categories(self, category, categories):
        def find_categories_gen(category, categories, found = False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_categories_gen(category, child, found)
                    if child == category and index+1 < len(categories) and type(categories[index+1]) == list:
                        flag = True
                        for i in categories[index+1]:
                            yield from find_categories_gen(category, i, flag)
            else:
                if category == categories or found == True:
                    yield categories
        
        return [i for i in find_categories_gen(category, categories)]
    
    def flatten(self, L):
        if type(L) in {list}:
            result = []
            for child in L:
                result.extend(self.flatten(child))
            return result
        else:
            return [L]

