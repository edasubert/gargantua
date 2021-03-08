# Gargantua - server
Sentence Aligner presented based on Fabienne Braune, Alexander Fraser. Source code of the aligner: https://github.com/braunefe/Gargantua

## Getting Started

Use the [Docker](https://www.docker.com/) image. Just run ```docker run -p 80:80 eduardsubert/gargantua```. This works on all platforms supported by Docker. (Run ```docker run -p 80:[PORT] eduardsubert/gargantua``` to publish the API to a ```[PORT]``` of your choice.)

By default, the aligner listens at http://localhost (unless you changed the published port) for POST requests. There is a documentation of the API at http://localhost/docs

Here's an example of how to use the API with CURL:

```bash
curl -X POST "http://localhost/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"source_tokenized\":\"Action taken on Parliament 's resolutions : see Minutes\Documents received : see Minutes\Written statements ( Rule 116 ) : see Minutes\Texts of agreements forwarded by the Council : see Minutes\Membership of Parliament : see Minutes\Membership of committees and delegations : see Minutes\Future action in the field of patents ( motions for resolutions tabled ) : see Minutes\Agenda for next sitting : see Minutes\Closure of sitting\",\"source_untokenized\":\"Action taken on Parliament's resolutions: see Minutes\Documents received: see Minutes\Written statements (Rule 116): see Minutes\Texts of agreements forwarded by the Council: see Minutes\Membership of Parliament: see Minutes\Membership of committees and delegations: see Minutes\Future action in the field of patents (motions for resolutions tabled): see Minutes\Agenda for next sitting: see Minutes\Closure of sitting\",\"target_tokenized\":\"Následný postup na základě usnesení Parlamentu : viz zápis\Předložení dokumentů : viz zápis\Písemná prohlášení ( článek 116 jednacího řádu ) : viz zápis\Texty smluv dodané Radou : viz zápis\Složení Parlamentu : viz zápis\Členství ve výborech a delegacích : viz zápis\Budoucí akce v oblasti patentů ( předložené návrhy usnesení ) : viz zápis\Pořad jednání příštího zasedání : viz zápis\Ukončení zasedání\",\"target_untokenized\":\"Následný postup na základě usnesení Parlamentu: viz zápis\Předložení dokumentů: viz zápis\Písemná prohlášení (článek 116 jednacího řádu): viz zápis\Texty smluv dodané Radou: viz zápis\Složení Parlamentu: viz zápis\Členství ve výborech a delegacích: viz zápis\Budoucí akce v oblasti patentů (předložené návrhy usnesení): viz zápis\Pořad jednání příštího zasedání: viz zápis\Ukončení zasedání\"}"
```
