# API_test_mini_dataguru

Mon API permet d'interagir avec une base de donnée d'images de tshirt et d'ajouter des tags à ces images.

Des requêtes GET pour des lectures de la base ou des requêtes POST pour des créations sur la base.

#Liste des actions:

_lecture de toute la table d'images de tshirts: localhost/images/tshirts/all

_Ajout d'une nouvelle image: localhost/images/tshirt + body={"tshirt_name":"...","type":"jpg|png|gif","url":"..."}

_Ajout d'un nouveau tag: localhost/images/tags + body={tag_name":"..."}

_Lecture de tous les tags: localhost/images/tags/all

_Ajout d'un tag à une image: localhost/tshirts/tags + body={"id_tag":...,"id_tshirt":...}

_Lecture de tous les tags d'une image: localhost/images/tshirts/id_tshirt/tags (où id_tshirt est l'id du tshirt voulu)

_Lecture de tous les tshirts ayant au moins 1 tag: localhost/images/tshirts/tags/all


