def get_segment(request):

    try:
        segment = "/".join(request.url.path.split("/")[1:])
        if segment == "":
            segment = "index"
        return f"/{segment}"
    except Exception as e:
        return e, dir(request.url)
        # return None
