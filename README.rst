===================================================
Generating Wiki Raga Articles using Knowledge Bases
===================================================

Wikipedia is the largest free online encyclopedia created and edited by volunteers around the world. Wikipedia supports multiple languages. Due to a large number of English speaking volunteers most information is available in English language, whereas several other local language wikis do not have adequate content. Motivating individuals to contribute to local Wikipedia can be effort intensive and time consuming without any guaranteed results. This project aims to improve content coverage in all languages (with a special focus on Indian languages). The overall system architecture is divided into three simple steps

   * KB Creation - Creating an enriched domain specific knowledge base. The KB design and enrichment process might involve domain expertise, human annotation, crowd sourcing and focused crawling.

   * Template creation - Creating a textual template for every domain and language pair so that meaningful and grammatically correct sentences can be generated from this KB.

   * Rendering content - Organizing the sentences and rendering them in a human-consumable format.


KB Creation
===========

* We create a domain specific KB for carnatic ragas which is stored on disk as JSON file in the form of a list of dictionaries, wherein, each dictionary holds the key: value pairs pertaining to on particular raga.

* Information about a raga is be either obtained from existing structured / semi-structured sources or generated automatically from its `moorchana`.

* List of ragams, moorchana, janaka-janya relations and kritis in ragas are obtained from `ragavardhini project <https://github.com/ssrihari/ragavardhini/>`__

* Other semistructured sources include `List of melakarta ragas and their chakras <https://en.wikipedia.org/wiki/Melakarta>`__, `varnams <http://www.carnatica.in/kriti/varnamlist.htm>`__, `List of Telugu movie songs set to a particular raga <http://rksanka.tripod.com/music/rslist.html>`__, `List of equivalent carnatic-hindustani raga pairs from <https://www.karnatik.com/hcragatable.shtml>`__.

* The values for the following attributes are computationally generated from raga moorchana.

   * Arohanam
   * Avarohanam
   * Janaka raga, chakra, melam / janaka_melam
   * Raga category

      * vakra
      * audava
      * shadava
      * sampoorna
      * audava-shadava
      * audava-sampoorna
      * shadava-sampoorna

   * Raga moorchana keyboard image
   * Raga moorchana audio
   * List of ragas with same arohanam
   * List of ragas with same avarohanam
   * List of ragas with one swara difference


* The commands required to generate the Wiki article texts as well as images and sounds for raga moorchana are given below.

.. code-block:: bash

   python create_kb.py --ragas resources/ragas.psv --kritis resources/kritis.psv --songs resources/songs.psv --varnams resources/varnams.psv --hind_ragas resources/hindustani.psv --chakras resources/chakra.psv --alternate_names resources/alternates.psv --transliteration resources/en_to_te.psv --config resources/config.json --result ragakb.json


.. code-block:: bash

   python render_moorchana.py --ragakb ragakb.json --config resources/config.json --img_path <path_to_op_img_dir> --audio_path <path_to_op_audio_dir>


Template Creation
=================

* We use Jinja2 template engine for creating templates for domain specific Wiki articles. Jinja2 is a powerful template engine which allows users to create diverse templates.

* The domain expert must create a template for every target domain. This template needs to be given as input to the rendering engine.

* The template contains variables who values need to be supplied from a python program. For this work, we create a template for carnatic ragas which is stored in templates/ragas.wiki


Rendering Articles
==================

* A python program takes an input the following artifacts to render the final wiki article.

   * Path to the KB
   * Path to domain specific jinja2 template
   * Result path where the text files should be stored

.. code-block:: bash

   python generate_wiki.py --kb_path ragakb.json --template_name ragas.wiki --result_path rendered_wiki/ragas/


Attribution
===========

* Nikhil Pattisapu - Main author of this repository.
* Patanjali Tallapragada - Provided the Telugu template for ragas. Manually corrected Eng-Tel transliteration outputs.
* PSL Prasanna Vibha - Manually corrected Eng-Tel transliteration outputs.
