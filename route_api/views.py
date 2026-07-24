from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RouteSerializer
from .services.optimization_service import optimize_route
from rest_framework import status

@api_view(['GET'])
def home(request):
    return Response({
        "message": "Fuel Route Optimizer API is running!"
    })

@api_view(["POST"])
def route_view(request):

    serializer = RouteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    try:
        result = optimize_route(
            data["start"],
            data["destination"]
        )

        return Response(result)

    except ValueError as e:

        return Response(
            {
                "error": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:

        return Response(
            {
                "error": "Internal server error.",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )