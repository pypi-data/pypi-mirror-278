#
# NOTICE:
#  This file contains views created during 'db-init'.
#

views = []

views.append(
    [
        "media",
        {
            "_id": "_design/filters",
            "views": {
                "by-name": {
                    "map": "function(doc) { \n  if (doc.metadata) {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, doc.metadata.duration]);\n  } else {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, null]);\n  }\n}"
                },
                "by-name-new": {
                    "map": "function(doc) { \n  if (doc.metadata && doc.play.status == 'new') {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, doc.metadata.duration]);\n  } else if (doc.play.status == 'new') {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, null]);\n  }\n}"
                },
                "by-name-played": {
                    "map": "function(doc) { \n  if (doc.metadata && doc.play.status == 'played') {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, doc.metadata.duration]);\n  } else if (doc.play.status == 'played') {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, null]);\n  }\n}"
                },
                "by-name-watched": {
                    "map": "function(doc) { \n  if (doc.metadata && doc.play.status == 'watched') {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, doc.metadata.duration]);\n  } else if (doc.play.status == 'watched') {\n    emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, null]);\n  }\n}"
                },
                "stats_sources": {
                    "map": "function (doc) {\n  emit(doc.sources, 1);\n}",
                    "reduce": "_count",
                },
                "stats_status": {
                    "map": "function (doc) {\n  emit(doc.play.status, 1);\n}",
                    "reduce": "_count",
                },
                "stats_total": {
                    "map": "function (doc) {\n  emit(doc._id, 1);\n}",
                    "reduce": "_count",
                },
            },
        },
    ]
)

views.append(
    [
        "injest_logs",
        {
            "_id": "_design/filters",
            "views": {
                "status": {
                    "map": "function (doc) {\n  emit([doc.batchid, doc.status, doc.reason], 1);\n}",
                    "reduce": "_count",
                }
            },
            "language": "javascript",
        },
    ]
)
