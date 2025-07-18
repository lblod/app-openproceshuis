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

;; -------------------------------------------------------------------------------------

(define-resource process()
  :class (s-prefix "dpv:Process")
  :properties `((:title :string ,(s-prefix "dct:title"))
                (:description :string ,(s-prefix "dct:description"))
                (:email :string ,(s-prefix "schema:email"))
                (:created :datetime ,(s-prefix "dct:created"))
                (:modified :datetime ,(s-prefix "dct:modified"))
                (:status :url ,(s-prefix "adms:status"))
                (:confidentiality-score :number ,(s-prefix "icr:confidentialityScore"))
                (:integrity-score :number ,(s-prefix "icr:integrityScore"))
                (:availability-score :number ,(s-prefix "icr:availabilityScore"))
                (:contains-personal-data :boolean ,(s-prefix "icr:containsPersonalData"))
                (:contains-professional-data :boolean ,(s-prefix "icr:containsProfessionalData"))
                (:contains-sensitive-personal-data :boolean ,(s-prefix "icr:containsSensitivePersonalData"))
                (:additional-information :string ,(s-prefix "icr:additionalInformation"))
                (:has-control-measure :url ,(s-prefix "icr:hasControlMeasure"))
                (:is-blueprint :boolean ,(s-prefix "icr:isBlueprint")))
  :has-one `((group :via ,(s-prefix "dct:publisher")
                    :as "publisher")
            (processStatistic :via ,(s-prefix "ext:hasStatistics")
                              :as "process-statistics"))
  :has-many `((file :via ,(s-prefix "nie:isPartOf")
                    :inverse t
                    :as "files")
              (ipdcProduct :via ,(s-prefix "cpsv:follows")
                           :inverse t
                           :as "ipdc-products")
              (administrative-unit-classification-codes :via ,(s-prefix "icr:isRelevantForAdministrativeUnit")
                                :as "relevant-administrative-units")
              (informationAsset :via ,(s-prefix "icr:hasInformationAsset")
                                :as "information-assets")
              (process :via ,(s-prefix "prov:wasInfluencedBy")
                       :as "linked-blueprints")
              (group :via ,(s-prefix "prov:usedBy")
                     :as "users"))
  :resource-base (s-url "http://data.lblod.info/processes/")
  :on-path "processes")

(define-resource processStatistic()
  :class (s-prefix "ext:ProcessStatistic")
  :properties `((:pdf-downloads :number ,(s-prefix "ext:pdfDownloads"))
                (:png-downloads :number ,(s-prefix "ext:pngDownloads"))
                (:svg-downloads :number ,(s-prefix "ext:svgDownloads"))
                (:bpmn-downloads :number ,(s-prefix "ext:bpmnDownloads"))
                (:visio-downloads :number ,(s-prefix "ext:visioDownloads"))
                (:process-views :number ,(s-prefix "ext:processViews")))
  :has-one `((process :via ,(s-prefix "ext:hasStatistics")
                      :inverse t
                      :as "process"))
  :resource-base (s-url "http://data.lblod.info/process-statistics/")
  :on-path "process-statistics")


(define-resource informationAsset()
  :class (s-prefix "skos:Concept")
  :properties `((:label :string ,(s-prefix "skos:prefLabel"))
                (:scheme :url ,(s-prefix "skos:inScheme")))
  :has-many `((process :via ,(s-prefix "icr:hasInformationAsset")
                       :inverse t
                       :as "processes"))
  :resource-base (s-url "http://data.lblod.info/information-assets/")
  :on-path "information-assets")

;; -------------------------------------------------------------------------------------
;; BPMN Based Ontology (BBO) (See https://www.irit.fr/recherches/MELODI/ontologies/BBO)
;; -------------------------------------------------------------------------------------

(define-resource bpmnElement ()
  :properties `((:name :string ,(s-prefix "bbo:name")))
  :has-one `((bpmnElementType :via ,(s-prefix "dct:type")
                              :as "type")
             (bpmnProcess :via ,(s-prefix "teamingAI:belongsToProcess")
                          :as "bpmn-process"))
  :on-path "bpmn-elements")

(define-resource bpmnElementType ()
  :class (s-prefix "skos:Concept")
  :properties `((:label :language-string ,(s-prefix "skos:prefLabel"))
                (:key :language-string ,(s-prefix "skos:hiddenLabel"))
                (:scheme :url ,(s-prefix "skos:inScheme")))
  :resource-base (s-url "http://lblod.data.gift/concepts/")
  :on-path "bpmn-element-types")

(define-resource bpmnProcess ()
  :class (s-prefix "bbo:Process")
  :has-one `((file :via ,(s-prefix "prov:wasDerivedFrom")
                   :as "bpmn-file"))
  :resource-base (s-url "http://data.lblod.info/bpmn-processes/")
  :on-path "bpmn-processes")

(define-resource task (bpmnElement)
  :class (s-prefix "bbo:Task")
  :resource-base (s-url "http://data.lblod.info/tasks/")
  :on-path "tasks")

(define-resource boundaryEvent (bpmnElement)
  :class (s-prefix "bbo:BoundaryEvent")
  :properties `((:reference :string ,(s-prefix "bbo:attachedToRef"))
                (:outgoing :string ,(s-prefix "bbo:has_outgoing"))
                (:eventDefinition :string ,(s-prefix "bbo:has_eventDefinition")))
  :resource-base (s-url "http://data.lblod.info/boundary-events/")
  :on-path "boundary-events")

(define-resource businessRuleTask (task)
  :class (s-prefix "bbo:BusinessRuleTask")
  :resource-base (s-url "http://data.lblod.info/business-rule-tasks/")
  :on-path "business-rule-tasks")

(define-resource endEvent (bpmnElement)
  :class (s-prefix "bbo:EndEvent")
  :properties `((:incoming :string ,(s-prefix "bbo:has_incoming")))
  :resource-base (s-url "http://data.lblod.info/end-events/")
  :on-path "end-events")

(define-resource errorEventDefinition (bpmnElement)
  :class (s-prefix "bbo:ErrorEventDefinition")
  :resource-base (s-url "http://data.lblod.info/error-event-defintions/")
  :on-path "error-event-defintions")

(define-resource error (bpmnElement)
  :class (s-prefix "bbo:Error")
  :resource-base (s-url "http://data.lblod.info/errors/")
  :on-path "errors")

(define-resource exclusiveGateway (bpmnElement)
  :class (s-prefix "bbo:ExclusiveGateway")
  :properties `((:defaultElement :string ,(s-prefix "bbo:has_defaultElement"))
                (:outgoing :string ,(s-prefix "bbo:has_outgoing"))
                (:incoming :string ,(s-prefix "bbo:has_incoming")))
  :resource-base (s-url "http://data.lblod.info/exclusive-gateways/")
  :on-path "exclusive-gateways")

(define-resource inclusiveGateway (bpmnElement)
  :class (s-prefix "bbo:InclusiveGateway")
  :properties `((:defaultElement :string ,(s-prefix "bbo:has_defaultElement"))
                (:outgoing :string ,(s-prefix "bbo:has_outgoing"))
                (:incoming :string ,(s-prefix "bbo:has_incoming")))
  :resource-base (s-url "http://data.lblod.info/inclusive-gateways/")
  :on-path "inclusive-gateways")

(define-resource intermediateThrowEvent (bpmnElement)
  :class (s-prefix "bbo:IntermediateThrowEvent")
  :properties `((:eventDefinition :string ,(s-prefix "bbo:has_eventDefinition"))
                (:outgoing :string ,(s-prefix "bbo:has_outgoing"))
                (:incoming :string ,(s-prefix "bbo:has_incoming")))
  :resource-base (s-url "http://data.lblod.info/intermediate-throw-events/")
  :on-path "intermediate-throw-events")

(define-resource manualTask (task)
  :class (s-prefix "bbo:ManualTask")
  :resource-base (s-url "http://data.lblod.info/manual-tasks/")
  :on-path "manual-tasks")

(define-resource messageEventDefinition (bpmnElement)
  :class (s-prefix "bbo:MessageEventDefinition")
  :resource-base (s-url "http://data.lblod.info/message-event-definitions/")
  :on-path "message-event-definitions")

(define-resource parallelGateway (bpmnElement)
  :class (s-prefix "bbo:ParallelGateway")
  :properties `((:defaultElement :string ,(s-prefix "bbo:has_defaultElement"))
                (:outgoing :string ,(s-prefix "bbo:has_outgoing"))
                (:incoming :string ,(s-prefix "bbo:has_incoming")))
  :resource-base (s-url "http://data.lblod.info/parallel-gateways/")
  :on-path "parallel-gateways")

(define-resource property (bpmnElement)
  :class (s-prefix "bbo:Property")
  :properties `((:propertyElement :string ,(s-prefix "bbo:has_property_element")))
  :resource-base (s-url "http://data.lblod.info/properties/")
  :on-path "properties")

(define-resource receiveTask (task)
  :class (s-prefix "bbo:ReceiveTask")
  :resource-base (s-url "http://data.lblod.info/receive-tasks/")
  :on-path "receive-tasks")

(define-resource scriptTask (task)
  :class (s-prefix "bbo:ScriptTask")
  :resource-base (s-url "http://data.lblod.info/script-tasks/")
  :on-path "script-tasks")

(define-resource sendTask (task)
  :class (s-prefix "bbo:SendTask")
  :resource-base (s-url "http://data.lblod.info/send-tasks/")
  :on-path "send-tasks")

(define-resource sequenceFlow (bpmnElement)
  :class (s-prefix "bbo:SequenceFlow")
  :properties `((:source :string ,(s-prefix "bbo:has_sourceRef"))
                (:target :string ,(s-prefix "bbo:has_targetRef")))
  :resource-base (s-url "http://data.lblod.info/sequence-flows/")
  :on-path "sequence-flows")

(define-resource serviceTask (task)
  :class (s-prefix "bbo:ServiceTask")
  :resource-base (s-url "http://data.lblod.info/service-tasks/")
  :on-path "service-tasks")

(define-resource startEvent (bpmnElement)
  :class (s-prefix "bbo:StartEvent")
  :properties `((:outgoing :string ,(s-prefix "bbo:has_outgoing")))
  :resource-base (s-url "http://data.lblod.info/start-events/")
  :on-path "start-events")

(define-resource subProcess (bpmnElement)
  :class (s-prefix "bbo:SubProcess")
  :properties `((:ramiLayer :uri ,(s-prefix "teamingAI:belongsToRAMILayer"))
                (:view :uri ,(s-prefix "teamingAI:belongsToView")))
  :resource-base (s-url "http://data.lblod.info/sub-processes/")
  :on-path "sub-processes")

(define-resource userTask (task)
  :class (s-prefix "bbo:UserTask")
  :resource-base (s-url "http://data.lblod.info/user-tasks/")
  :on-path "user-tasks")

;; -------------------------------------------------------------------------------------
;; BBO Extension
;; -------------------------------------------------------------------------------------

(define-resource association (bpmnElement)
  :class (s-prefix "bboExtension:Association")
  :properties `((:source :string ,(s-prefix "bbo:has_sourceRef"))
                (:target :string ,(s-prefix "bbo:has_targetRef")))
  :resource-base (s-url "http://data.lblod.info/associations/")
  :on-path "associations")

(define-resource collaboration (bpmnElement)
  :class (s-prefix "bboExtension:Collaboration")
  :resource-base (s-url "http://data.lblod.info/collaborations/")
  :on-path "collaborations")

(define-resource dataInputAssociation (bpmnElement)
  :class (s-prefix "bboExtension:DataInputAssociation")
  :properties `((:source :string ,(s-prefix "bbo:has_sourceRef"))
                (:target :string ,(s-prefix "bbo:has_targetRef"))
                (:dataInputFor :string ,(s-prefix "bboExtension:is_dataInputFor")))
  :resource-base (s-url "http://data.lblod.info/data-input-associations/")
  :on-path "data-input-associations")

(define-resource dataObject (bpmnElement)
  :class (s-prefix "bboExtension:DataObject")
  :resource-base (s-url "http://data.lblod.info/data-objects/")
  :on-path "data-objects")

(define-resource dataObjectReference (bpmnElement)
  :class (s-prefix "bboExtension:DataObjectReference")
  :properties `((:reference :string ,(s-prefix "bboExtension:dataObjectRef")))
  :resource-base (s-url "http://data.lblod.info/data-object-references/")
  :on-path "data-object-references")

(define-resource dataOutputAssociation (bpmnElement)
  :class (s-prefix "bboExtension:DataOutputAssociation")
  :properties `((:target :string ,(s-prefix "bbo:has_targetRef"))
                (:dataOutputFrom :string ,(s-prefix "bboExtension:is_dataOutputFrom")))
  :resource-base (s-url "http://data.lblod.info/data-output-associations/")
  :on-path "data-output-associations")

(define-resource dataStoreReference (bpmnElement)
  :class (s-prefix "bboExtension:DataStoreReference")
  :resource-base (s-url "http://data.lblod.info/data-store-references/")
  :on-path "data-store-references")

(define-resource lane (bpmnElement)
  :class (s-prefix "bboExtension:Lane")
  :properties `((:activity :string ,(s-prefix "bbo:has_activity")))
  :resource-base (s-url "http://data.lblod.info/lanes/")
  :on-path "lanes")

(define-resource laneSet (bpmnElement)
  :class (s-prefix "bboExtension:LaneSet")
  :resource-base (s-url "http://data.lblod.info/lane-sets/")
  :on-path "lane-sets")

(define-resource messageFlow (bpmnElement)
  :class (s-prefix "bboExtension:MessageFlow")
  :properties `((:source :string ,(s-prefix "bbo:has_sourceRef"))
                (:target :string ,(s-prefix "bbo:has_targetRef")))
  :resource-base (s-url "http://data.lblod.info/message-flows/")
  :on-path "message-flows")

(define-resource participant (bpmnElement)
  :class (s-prefix "bboExtension:Participant")
  :properties `((:process :string ,(s-prefix "bboExtension:processRef")))
  :resource-base (s-url "http://data.lblod.info/participants/")
  :on-path "participants")

(define-resource textAnnotation (bpmnElement)
  :class (s-prefix "bboExtension:TextAnnotation")
  :properties `((:comment :string ,(s-prefix "rdfs:comment")))
  :resource-base (s-url "http://data.lblod.info/text-annotations/")
  :on-path "text-annotations")
