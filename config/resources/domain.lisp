(in-package :mu-cl-resources)

(defparameter *include-count-in-paginated-responses* t)
(defparameter sparql:*experimental-no-application-graph-for-sudo-select-queries* t)
(defparameter *default-page-size* 20)

; Caching
(defparameter *cache-model-properties* t)
(defparameter *cache-count-queries* t)
(defparameter *supply-cache-headers-p* t)

(defparameter *use-custom-boolean-type-p* nil)

(read-domain-file "auth.json")
(read-domain-file "job.lisp")
(read-domain-file "file.lisp")
(read-domain-file "report.lisp")
(read-domain-file "ipdc.lisp")
(read-domain-file "conceptual-process.lisp")
(read-domain-file "process.lisp")
(read-domain-file "process-step.lisp")
(read-domain-file "statistic.lisp")
