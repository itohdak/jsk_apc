#!/usr/bin/env roseus
(load "package://baxtereus/baxter-interface.l")
(load "package://jsk_2014_picking_challenge/euslisp/utils.l")
(load "package://jsk_2014_picking_challenge/euslisp/arm-motion.l")
(load "package://jsk_2014_picking_challenge/euslisp/target-pick-region.l")
(load "package://jsk_2014_picking_challenge/euslisp/pod-lowres.l")
(load "package://jsk_2014_picking_challenge/euslisp/order-bin.l")
(load "package://jsk_2014_picking_challenge/euslisp/gripper-control.l")

(defun init ()
  (baxter-init)
  (send *baxter* :locate #f(0 0 950) :world)
  (send *baxter* :angle-vector (send *ri* :state :potentio-vector))
  (pod-init)
  (orderbin-init)
  (objects (list *baxter* *pod* *orderbin*)))

(defun test-for-bin (arm bin)
  (ros::ros-info "test for ~A" bin)
  (move-to-target-bin arm bin)
  (pick-object arm)
  (move-to-order-bin arm))

(defun test (arm)
  (let (bins)
    (case arm
      (:rarm (setq bins (list :b :c :e :f :h :i :k :l)))
      (:larm (setq bins (list :a :d :g :j))))
    (dolist (bin bins) (test-for-bin arm bin))
    ))

(init)
