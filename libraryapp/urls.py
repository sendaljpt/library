from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import StudentList, LibrarianList, BookList, BorrowingRecordList, BorrowBookView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('students/', StudentList.as_view(), name='student-list'),
    path('librarians/', LibrarianList.as_view(), name='librarian-list'),
    path('books/', BookList.as_view(), name='book-list'),
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('borrowing-records/', BorrowingRecordList.as_view(), name='borrowing-record-list'),
]