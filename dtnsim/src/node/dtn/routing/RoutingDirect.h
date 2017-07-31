
#ifndef SRC_NODE_DTN_ROUTINGDIRECT_H_
#define SRC_NODE_DTN_ROUTINGDIRECT_H_

#include <dtn/routing/RoutingDeterministic.h>
#include <dtn/SdrModel.h>

class RoutingDirect : public RoutingDeterministic
{
public:
	RoutingDirect(int eid, SdrModel * sdr, ContactPlan * contactPlan);
	virtual ~RoutingDirect();
	virtual void routeAndQueueBundle(BundlePkt *bundle, double simTime);
};

#endif /* SRC_NODE_DTN_ROUTINGDIRECT_H_ */
