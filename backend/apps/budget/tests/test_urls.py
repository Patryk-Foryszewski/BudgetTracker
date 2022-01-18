from django.test import TestCase
from django.urls import resolve, reverse


class UrlTester(TestCase):
    def test_budget_create_url(self):
        path = "/api/v1/budget/create/"
        path_name = "budget:create"
        view_name = "BudgetCreate"
        self.assertEqual(reverse(path_name), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_update_url(self):
        args = [1]
        path = "/api/v1/budget/1/update/"
        path_name = "budget:update"
        view_name = "BudgetUpdate"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_list_url(self):
        path = "/api/v1/budget/list/"
        path_name = "budget:list"
        view_name = "BudgetList"
        self.assertEqual(reverse(path_name), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_detail_url(self):
        args = [1]
        path = "/api/v1/budget/1/detail/"
        path_name = "budget:detail"
        view_name = "BudgetDetail"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_delete_url(self):
        args = [1]
        path = "/api/v1/budget/1/delete/"
        path_name = "budget:delete"
        view_name = "BudgetDelete"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_remove_participants_url(self):
        args = [1]
        path = "/api/v1/budget/1/remove_participants/"
        path_name = "budget:remove_participants"
        view_name = "BudgetRemoveParticipants"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_create_expense_url(self):
        args = [1]
        path = "/api/v1/budget/1/create_expense/"
        path_name = "budget:create_expense"
        view_name = "ExpenseCreate"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_update_expense_url(self):
        args = [1]
        path = "/api/v1/budget/update_expense/1/"
        path_name = "budget:update_expense"
        view_name = "ExpenseUpdate"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_create_category_url(self):
        args = [1]
        path = "/api/v1/budget/1/create_category/"
        path_name = "budget:create_category"
        view_name = "CategoryCreate"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_list_category_url(self):
        args = [1]
        path = "/api/v1/budget/1/list_category/"
        path_name = "budget:list_category"
        view_name = "CategoryList"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_edit_category_url(self):
        args = [1]
        path = "/api/v1/budget/edit_category/1/"
        path_name = "budget:edit_category"
        view_name = "CategoryEdit"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)

    def test_budget_delete_category_url(self):
        args = [1]
        path = "/api/v1/budget/delete_category/1/"
        path_name = "budget:delete_category"
        view_name = "CategoryDelete"
        self.assertEqual(reverse(path_name, args=args), path)
        resolver = resolve(path)
        self.assertEqual(resolver.func.__name__, view_name)
