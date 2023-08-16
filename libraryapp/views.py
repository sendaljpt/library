from rest_framework import generics
from rest_framework import permissions
from .models import Student, Librarian, Book, BorrowingRecord
from .serializers import StudentSerializer, LibrarianSerializer, BookSerializer, BorrowingRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class LibrarianList(generics.ListCreateAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowingRecordList(generics.ListAPIView):
    
    permission_classes = [permissions.IsAuthenticated] 
    
    def get(self, request, *args, **kwargs):
        queryset = BorrowingRecord.objects.filter(student=request.user.student)
        
        serializer = BorrowingRecordSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BorrowBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        book_id = request.data.get('book_id')  
        student = request.user.student

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        if book.available_copies <= 0:
            return Response({"error": "Book is not available for borrowing."}, status=status.HTTP_400_BAD_REQUEST)
        
        # get lates borrowing
        latestBorrowing = BorrowingRecord.objects.filter(student=student, book=book_id, returned=False)
        if latestBorrowing:
            return Response({"error": "You must return this book first."}, status=status.HTTP_400_BAD_REQUEST)

        borrowing_record = BorrowingRecord.objects.create(student=student, book=book)
        book.available_copies -= 1
        book.save()

        serializer = BorrowingRecordSerializer(borrowing_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)